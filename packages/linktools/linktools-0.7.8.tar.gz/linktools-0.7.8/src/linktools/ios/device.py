#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Author    : HuJi <jihu.hj@alibaba-inc.com>
# Datetime  : 2022/2/25 6:30 PM
# User      : huji
# Product   : PyCharm
# Project   : link

import asyncio
import copy
import threading
from asyncio import StreamReader, StreamWriter
from typing import Union, Optional

import tidevice

from .. import get_logger, utils

_logger = get_logger("ios.device")

MuxError = tidevice.MuxError


class Usbmux(tidevice.Usbmux):
    __default_usbmux = tidevice.Usbmux()

    @classmethod
    def set_default(cls, usbmux: Union["Usbmux", str]):
        if isinstance(usbmux, str):
            cls.__default_usbmux = Usbmux(usbmux)
        elif isinstance(usbmux, Usbmux):
            cls.__default_usbmux = usbmux

    @classmethod
    def get_default(cls):
        return cls.__default_usbmux


Usbmux.set_default(Usbmux())


class Device(tidevice.Device):

    def __init__(self, udid: Optional[str] = None, usbmux: Union[Usbmux, str, None] = None):
        super().__init__(udid, usbmux or Usbmux.get_default())

    def forward(self, local_port: int, remote_port: int, local_address: str = "127.0.0.1"):
        return _ForwardThread(self, local_address, local_port, remote_port)

    def __copy__(self):
        return Device(self.udid, self.usbmux)


class _ForwardThread(threading.Thread):

    def __init__(self, device: "Device", local_address: str, local_port: int, remote_port: int):
        super().__init__()
        self._device = device
        self._local_address = local_address
        self._local_port = local_port
        self._remote_port = remote_port

        self._loop = None
        self._stopped = False
        self._stop_event = None
        self._stop_event_task = None
        self._lock = threading.RLock()

    def run_forever(self):
        try:
            self.start()
            while True:
                self.join(1)
        except KeyboardInterrupt:
            self.stop()
        finally:
            self.join()

    def stop(self):
        with self._lock:
            if self._stopped:
                return
            self._stopped = True
            if self._loop and self._stop_event:
                self._loop.call_soon_threadsafe(self._stop_event.set)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.stop()
        self.join()

    def run(self):
        with self._lock:
            if self._stopped:
                return
            loop = self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            event = self._stop_event = asyncio.Event()
            task = self._stop_event_task = loop.create_task(event.wait())

        server = None
        try:
            coro = asyncio.start_server(self._handle_client, self._local_address, self._local_port)
            server = loop.run_until_complete(coro)
            _logger.debug(f"Usbmux proxy serving on {server.sockets[0].getsockname()} => {self._remote_port}")
            loop.run_until_complete(task)

        except BaseException as e:
            _logger.error(f"Usbmux proxy error: {e}")

        finally:
            with self._lock:
                self._stopped = True
                self._loop.call_soon(self._stop_event.set)

            if server:
                _logger.debug(f"Usbmux proxy close")
                server.close()
                loop.run_until_complete(server.wait_closed())

            tasks = asyncio.all_tasks(loop=loop) \
                if hasattr(asyncio, "all_tasks") \
                else asyncio.Task.all_tasks(loop=loop)
            for task in tasks:
                utils.ignore_error(loop.run_until_complete, task)
            loop.close()

    async def _handle_client(self, client_reader: StreamReader, client_writer: StreamWriter):

        client_address = client_writer.get_extra_info('peername')
        _logger.debug(f"Handle client request: {client_address}")

        pending_tasks, finished = None, asyncio.Event()
        plist_socket, usbmux_reader, usbmux_writer = None, None, None

        try:
            device = copy.copy(self._device)
            plist_socket = device.create_inner_connection(self._remote_port)
            usbmux_reader, usbmux_writer = await asyncio.open_connection(sock=plist_socket.get_socket())

            _, pending_tasks = await asyncio.wait([
                asyncio.create_task(self._handle_forward_stream(usbmux_reader, client_writer)),
                asyncio.create_task(self._handle_forward_stream(client_reader, usbmux_writer)),
                asyncio.create_task(self._handle_close_stream((client_writer, usbmux_writer), finished)),
            ], return_when=asyncio.FIRST_COMPLETED)

        except tidevice.MuxError as e:
            _logger.debug(f"connect to device error: {e}")

        finally:
            finished.set()

            if pending_tasks:
                await asyncio.wait(pending_tasks)
            if usbmux_writer:
                await self._close_stream(usbmux_writer)
            if client_writer:
                await self._close_stream(client_writer)
            if plist_socket:
                plist_socket.close()

            _logger.debug(f"handle client proxy request finished: {client_address}")

    async def _handle_forward_stream(self, reader: StreamReader, writer: StreamWriter):
        while not self._stop_event.is_set():
            try:
                data = await reader.read(1024 * 10)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
            except Exception as e:
                _logger.debug(f"forward stream error: {e}")
                break

    async def _handle_close_stream(self, writers: [StreamWriter], event):
        await asyncio.wait([
            self._stop_event_task,
            asyncio.create_task(event.wait())
        ], return_when=asyncio.FIRST_COMPLETED)
        await asyncio.wait(
            [asyncio.create_task(self._close_stream(w)) for w in writers],
        )

    @classmethod
    async def _close_stream(cls, writer: StreamWriter):
        try:
            writer.close()
            if hasattr(writer, "wait_closed"):
                await writer.wait_closed()
        except Exception as e:
            _logger.debug(f"Close stream error: {e}")
