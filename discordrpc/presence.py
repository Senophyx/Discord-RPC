import sys
import os
import socket
import json
import struct
import uuid
import re
import time
from .exceptions import *
from .utils import remove_none


OP_HANDSHAKE = 0
OP_FRAME = 1
OP_CLOSE = 2



class RPC:
    def __init__(self, app_id:int):
        app_id = str(app_id)
        self.app_id = app_id

        self.debug = True
        # Soon :
        # self.show_output = False
        # self.is_connected = False
        # self.is_running = False

        if sys.platform == "win32":
            self.ipc = WindowsPipe(app_id, self.debug)
            self.ipc.handshake()

        else:
            self.ipc = UnixPipe(app_id, self.debug)
            self.ipc.handshake()



    timestamp = time.time()
    

    def set_activity(
            self,
            state: str=None, details:str=None,
            start: int=None, end: int = None,
            large_image:str=None, large_text:str=None,
            small_image:str=None, small_text:str=None,
            party_id:str=None, party_size: list=None,
            join_secret:str=None, spectate_secret:str=None,
            match_secret:str=None, buttons=None
        ):

        act = {
            "state": state,
            "details": details,
            "timestamps": {
                "start": start,
                "end": end
            },
            "assets": {
                "large_image": large_image,
                "large_text": large_text,
                "small_image": small_image,
                "small_text": small_text
            },
            "party": {
                "id": party_id,
                "size": party_size
            },
            "secrets": {
                "join": join_secret,
                "spectate": spectate_secret,
                "match": match_secret
            },
            "buttons": buttons
        }


        payload = {
            'cmd': 'SET_ACTIVITY',
            'args': {
                'pid': os.getpid(),
                'activity': remove_none(act)
            },
            'nonce': str(uuid.uuid4())
        }

        self.ipc._send(payload, OP_FRAME)

    
    def disconnect(self):
        self.ipc.disconnect()




class WindowsPipe:
    def __init__(self, app_id, debug):
        self.app_id = app_id
        self.debug = debug

        base_path = R'\\?\pipe\discord-ipc-{}'
        
        for i in range(10):
            path = base_path.format(i)

            try:
                self.socket = open(path, "w+b")
            except OSError as e:
                raise Error("Failed to open {!r}: {}".format(path, e))
            else:
                break

        else:
            raise DiscordNotOpened()
        
        if self.debug == True:
            print(f"Connected to {path}")


    def _recv(self):
        enc_header = b''
        header_size = 8

        while header_size:
            enc_header += self.socket.read(header_size)
            header_size -= len(enc_header)

        dec_header = struct.unpack("<ii", enc_header)
        enc_data = b''
        remain_packet_size = int(dec_header[1])

        while remain_packet_size:
            enc_data += self.socket.read(remain_packet_size)
            remain_packet_size -= len(enc_data)
        
        
        output = json.loads(enc_data.decode('UTF-8'))

        if self.debug == True:
            print(output)

        return output
    

    def _send(self, payload, op=OP_FRAME):
        if self.debug == True:
            print(payload)

        payload = json.dumps(payload).encode('UTF-8')
        payload = struct.pack('<ii', op, len(payload)) + payload

        self.socket.write(payload)
        self.socket.flush()


    def handshake(self):
        self._send({'v': 1, 'client_id': self.app_id}, op=OP_HANDSHAKE)
        data = self._recv()

        if data['cmd'] == 'DISPATCH' and data['evt'] == 'READY':
            print(f"Connected to {data['data']['user']['global_name']} ({data['data']['user']['username']}) | User ID : {data['data']['user']['id']}")
            return True
        
        else:
            if data['code'] == 4000:
                raise InvalidID
            

    def disconnect(self):
        self._send({}, OP_CLOSE)
        
        self.socket.close()
        self.socket = None
        print("Closing")
        exit()



class UnixPipe:
    def __init__(self, app_id, debug):
        self.app_id = app_id
        self.debug = debug

        self.socket = socket.socket(socket.AF_UNIX)

        base_path = path = os.environ.get('XDG_RUNTIME_DIR') or os.environ.get('TMPDIR') or os.environ.get('TMP') or os.environ.get('TEMP') or '/tmp'
        base_path = re.sub(r'\/$', '', path) + '/discord-ipc-{0}'

        for i in range(10):
            path = base_path.format(i)

            try:
                self.socket.connect(path)
                break
            except FileNotFoundError:
                pass

        else:
            raise DiscordNotOpened()
        
        if self.debug == True:
            print(f"Connected to {path}")


    def _recv(self):
        recv_data = self.socket.recv(1024)
        enc_header = recv_data[:8]
        dec_header = struct.unpack("<ii", enc_header)
        enc_data = recv_data[8:]

        output = json.loads(enc_data.decode('UTF-8'))
    
        if self.debug == True:
            print(output)

        return output
    

    def _send(self, payload, op=OP_FRAME):
        if self.debug == True:
            print(payload)

        payload = json.dumps(payload).encode('UTF-8')
        payload = struct.pack('<ii', op, len(payload)) + payload

        self.socket.send(payload)

    
    def handshake(self):
        self._send({'v': 1, 'client_id': self.app_id}, op=OP_HANDSHAKE)
        data = self._recv()

        if data['cmd'] == 'DISPATCH' and data['evt'] == 'READY':
            print(f"Connected to {data['data']['user']['global_name']} ({data['data']['user']['username']}) | User ID : {data['data']['user']['id']}")
            return True
        
        else:
            if data['code'] == 4000:
                raise InvalidID()
            

    def disconnect(self):
        self._send({}, OP_CLOSE)

        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        self.socket = None
        print("Closing")
        exit()