import json
import os
import socket
import sys
import struct
import time
from .exceptions import *


OP_HANDSHAKE = 0
OP_FRAME = 1
OP_CLOSE = 2
OP_PING = 3
OP_PONG = 4


class RPC:
    def __init__(self, client_id):
        self.client_id = client_id
        self._connect()
        self._do_handshake()
        self._output = None
        self.show_output = False


    @classmethod
    def set_id(self, app_id):
        app_id = str(app_id)
        platform = sys.platform
        if platform == 'win32':
            return DiscordWindows(app_id)
        else:
            return DiscordUnix(app_id)
        
    
    def _connect(self):
        pass


    def _do_handshake(self):
        op, data = self.send_recv({'v': 1, 'client_id': self.client_id}, op=OP_HANDSHAKE)
        if op == OP_FRAME and data['cmd'] == 'DISPATCH' and data['evt'] == 'READY':
            return
        else:
            if op == OP_CLOSE:
                self.close()
            raise RuntimeError(data)
        

    def _write(self, data:bytes):
        pass

    def _recv(self, size:int) -> bytes:
        pass

    def _recv_header(self):
        header = self._recv_exact(8)
        return struct.unpack("<II", header)
    
    def _recv_exact(self, size_remaining) -> bytes:
        buf = b""
        while size_remaining:
            chunk = self._recv(size_remaining)
            buf += chunk
            size_remaining -= len(chunk)
        return buf
    
    def close(self):
        try:
            self.send({}, op=OP_CLOSE)
        finally:
            self._close()

    
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
        data = json.dumps(data, separators=(',', ':')).encode('UTF-8')
        header = struct.pack("<II", op, len(data))
        self._write(header)
        self._write(data)

    def recv(self):
        op, length = self._recv_header()
        payload = self._recv_exact(length)
        data = json.loads(payload.decode('UTF-8'))
        return op, data
    
    timestamp = time.mktime(time.localtime())
    
    def set_activity(
            self,
            state:str=None,
            details:str=None,
            timestamp=None,
            small_text:str='null',
            large_text:str='null',
            small_image:str='null',
            large_image:str='null',
            buttons=None
    ):
        
        if len(large_text) <= 1:
            raise Error('"large text" must be at least above 1 characters')
        
        if len(small_text) <= 1:
            raise Error('"small text" must be at least above 1 characters')
        
        act = {
            "state": state,
            "details": details,
            "timestamps": {
                "start": timestamp
            },
            "assets": {
                "small_text": small_text,
                "large_text": large_text,
                "small_image": str(small_image),
                "large_image": str(large_image)
            },
            "buttons": buttons,
        }

        if state == None or state == '' or state == 'null':
            act.pop('state', None)
        if details == None or details == '' or details == 'null':
            act.pop('details', None)
        if small_text == None or small_text == '' or small_text == 'null':
            act['assets'].pop('small_text', None)
        if large_text == None or large_text == '' or large_text == 'null':
            act['assets'].pop('large_text', None)
        if timestamp == None:
            act.pop('timestamps', None)
        if buttons == None:
            act.pop('buttons', None)


        data = {
            'cmd': 'SET_ACTIVITY',
            'args': {
                'pid': os.getpid(),
                'activity': act
            },
            'nonce': '{:.20f}'.format(time.time())
        }

        self.send(data)

        op, length = self._recv_header()
        payload = self._recv_exact(length)
        output = json.loads(payload.decode('UTF-8'))
        if output['evt'] == 'ERROR':
            raise ActivityError
        
        else:
            if self.show_output==True:print(f"Successfully set RPC for {self.client_id}")

        return op, output

    

    def run(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.close()



class DiscordWindows(RPC):
    _pipe_path = R'\\?\pipe\discord-ipc-{}'

    def _connect(self):
        for i in range(10):
            path = self._pipe_path.format(i)

            try:
                self._open = open(path, "w+b")
            except OSError as e:
                raise Error("Failed to open {!r}: {}".format(path, e))
            else:
                break

        else:
            raise DiscordNotOpened

        self.path = path

    def _write(self, data:bytes):
        self._open.write(data)
        self._open.flush()

    def _recv(self, size:int) -> bytes:
        return self._open.read(size)
    
    def _close(self):
        self._open.close()



class DiscordUnix(RPC):
    def _connect(self):
        self._socket = socket.socket(socket.AF_UNIX)
        pipe_path = self._get_pipe_path()

        for i in range(10):
            path = pipe_path.format(i)
            if not os.path.exists(path):
                continue
            try:
                self._socket.connect(path)
            except OSError as e:
                raise Error("Failed to open {!r}: {}".format(path, e))
            else:
                break
        else:
            raise DiscordNotOpened


    def _get_pipe_path():
        env_keys = ('XDG_RUNTIME_DIR', 'TMPDIR', 'TMP', 'TEMP')
        for env_key in env_keys:
            dir_path = os.environ.get(env_key)
            if dir_path:
                break
        else:
            dir_path = '/tmp'
        return os.path.join(dir_path, 'discord-ipc-{}')
    

    def _write(self, data:bytes):
        self._socket.sendall(data)

    def _recv(self, size:int) -> bytes:
        return self._socket.recv(size)
    
    def _close(self):
        self._socket.close()
