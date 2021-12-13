from abc import ABCMeta, abstractmethod
import json
import logging
import os
import socket
import sys
import struct
import uuid
import time
from time import mktime

OP_HANDSHAKE = 0
OP_FRAME = 1
OP_CLOSE = 2
OP_PING = 3
OP_PONG = 4

logger = logging.getLogger(__name__)


class DiscordIpcError(Exception):
    pass


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
        logger.info("connected via ID %s", client_id)

    @classmethod
    def Set_ID(cls, app_id):
        r"""
        A Classmethod to set applications ID
        """
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
        state:str, 
        details:str,
        timestamp, 
        small_text:str, 
        large_text:str,
        small_image:str=None, 
        large_image:str=None
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
        """
        if large_image == None:
           large_image = 'Not_Set'
           print("Warning, Large Image not set, but RPC will still working properly")
        if small_image == None:
            small_image = 'Not_Set'
            print("Warning, Small Image not set, but RPC will still working properly")
        else:
            pass

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

        data = {
            'cmd': 'SET_ACTIVITY',
            'args': {'pid': os.getpid(),
                     'activity': act},
            'nonce': str(uuid.uuid4())
        }

        self.send(data)
        print("Succsessfully set RPC")


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
            return DiscordIpcError("Failed to connect to Discord pipe")

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
            return DiscordIpcError("Failed to connect to Discord pipe")

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
