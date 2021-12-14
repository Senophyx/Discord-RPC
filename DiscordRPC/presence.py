from abc import ABCMeta, abstractmethod
import json
import logging
import os
import socket
import sys
import struct
from datetime import datetime
import time
from time import mktime

from .exceptions import *

OP_HANDSHAKE = 0
OP_FRAME = 1
OP_CLOSE = 2
OP_PING = 3
OP_PONG = 4

logger = logging.getLogger(__name__)


class RPC(metaclass=ABCMeta):

    r"""A class that implements RPC
    -----------
    Classmethod :
    - Set_ID: :class:`str` | set your applications ID
    """

    def __init__(self, client_id):
        self.client_id = client_id
        self._connect()
        self._do_handshake()
        self.get_output = None
        logger.info("connected via ID %s", client_id)

    @classmethod
    def Set_ID(cls, app_id):
        r"""
        A Classmethod to set applications ID
        """
        app_id = str(app_id) # Because ID must be string, so I tricked with this.
        platform=sys.platform
        if platform == 'win32':
            return DiscordWindows(app_id)
        else:
            return DiscordUnix(app_id)

    @abstractmethod
    def _connect(self):
        pass

    def _do_handshake(self):
        ret_op, ret_data = self.send_recv({'v': 1, 'client_id': self.client_id}, op=OP_HANDSHAKE)
        if ret_op == OP_FRAME and ret_data['cmd'] == 'DISPATCH' and ret_data['evt'] == 'READY':
            return
        else:
            if ret_op == OP_CLOSE:
                self.close()
            raise RuntimeError(ret_data)

    @abstractmethod
    def _write(self, date: bytes):
        pass

    @abstractmethod
    def _recv(self, size: int) -> bytes:
        pass

    def _recv_header(self):
        header = self._recv_exactly(8)
        return struct.unpack("<II", header)

    def _recv_exactly(self, size) -> bytes:
        buf = b""
        size_remaining = size
        while size_remaining:
            chunk = self._recv(size_remaining)
            buf += chunk
            size_remaining -= len(chunk)
        return buf

    def close(self):
        logger.warning("closing connection")
        try:
            self.send({}, op=OP_CLOSE)
        finally:
            self._close()

    @abstractmethod
    def _close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def send_recv(self, data, op=OP_FRAME):
        self.send(data, op)
        return self.recv()

    def send(self, data, op=OP_FRAME):
        logger.debug("sending %s", data)
        data_str = json.dumps(data, separators=(',', ':'))
        data_bytes = data_str.encode('utf-8')
        header = struct.pack("<II", op, len(data_bytes))
        self._write(header)
        self._write(data_bytes)

    def recv(self):
        """Receives a packet from discord.
        Returns op code and payload.
        """
        op, length = self._recv_header()
        payload = self._recv_exactly(length)
        data = json.loads(payload.decode('utf-8'))
        logger.debug("received %s", data)
        return op, data

    def timestamp(self):
        timestamp = mktime(time.localtime())
        return timestamp

    def set_activity(
        self, 
        state:str=None, 
        details:str=None,
        timestamp=None, 
        small_text:str=None, 
        large_text:str=None,
        small_image:str=None, 
        large_image:str=None,
        buttons=None
    ): 

        r"""
        A method for set RPC activity
        -------
        Parameters :
        - state: `str`
        - details: `str`
        - timestamp: `You can use timestamp method`
        - small_text: `str`
        - large_text: `str`
        - small_image: `str` | must be the same as image name in application assets
        - large_image: `str` | must be the same as image name in application assets
        - buttons: `str` | use DiscordRPC.button() method
        """
        
        if large_image == None:
           large_image = 'null'
        if small_image == None:
            small_image = 'null'
        if small_text == None:
            small_text = 'null'
        if large_text == None:
            large_text = 'null'
        else:
            if len(large_text) <= 3:
                raise Error('"large text" must be at least above 3 characters')

            if len(small_text) <= 3:
                raise Error('"small text" must be at least above 3 characters')

        if buttons == None:
            act = {
            "state": state,
            "details": details,
            "timestamps": {
                "start": timestamp
            },
            "assets": {
                "small_text": small_text,
                "small_image": str(small_image),
                "large_text": large_text,
                "large_image": str(large_image)
            }
        }

        else:
            act = {
                "state": state,
                "details": details,
                "timestamps": {
                    "start": timestamp
                },
                "assets": {
                    "small_text": small_text,
                    "small_image": str(small_image),
                    "large_text": large_text,
                    "large_image": str(large_image)
                },
                "buttons": buttons,
            }

        data = {
            'cmd': 'SET_ACTIVITY',
            'args': {'pid': os.getpid(),
                     'activity': act},
            'nonce': datetime.now().strftime("%D - %H:%M:%S")
        }

        self.send(data)

        op, length = self._recv_header()
        payload = self._recv_exactly(length)
        output = json.loads(payload.decode('utf-8'))
        self.get_output = output

        if output['evt'] == "ERROR":
            raise ActivityError
        else:
            print("Successfully set RPC")

        return op, output

    def output(self):
        output = self.get_output
        return output


class DiscordWindows(RPC):

    _pipe_pattern = R'\\?\pipe\discord-ipc-{}'

    def _connect(self):
        for i in range(10):
            path = self._pipe_pattern.format(i)
            try:
                self._f = open(path, "w+b")
            except OSError as e:
                logger.error("failed to open {!r}: {}".format(path, e))
            else:
                break
        else:
            raise DiscordNotOpened

        self.path = path

    def _write(self, data: bytes):
        self._f.write(data)
        self._f.flush()

    def _recv(self, size: int) -> bytes:
        return self._f.read(size)

    def _close(self):
        self._f.close()


class DiscordUnix(RPC):

    def _connect(self):
        self._sock = socket.socket(socket.AF_UNIX)
        pipe_pattern = self._get_pipe_pattern()

        for i in range(10):
            path = pipe_pattern.format(i)
            if not os.path.exists(path):
                continue
            try:
                self._sock.connect(path)
            except OSError as e:
                logger.error("failed to open {!r}: {}".format(path, e))
            else:
                break
        else:
            raise DiscordNotOpened

    @staticmethod
    def _get_pipe_pattern():
        env_keys = ('XDG_RUNTIME_DIR', 'TMPDIR', 'TMP', 'TEMP')
        for env_key in env_keys:
            dir_path = os.environ.get(env_key)
            if dir_path:
                break
        else:
            dir_path = '/tmp'
        return os.path.join(dir_path, 'discord-ipc-{}')

    def _write(self, data: bytes):
        self._sock.sendall(data)

    def _recv(self, size: int) -> bytes:
        return self._sock.recv(size)

    def _close(self):
        self._sock.close()
