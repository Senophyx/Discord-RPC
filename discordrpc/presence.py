import sys
import os
import socket
import json
import struct
import uuid
import re
from .exceptions import *
from .types import *
from .utils import *
import logging
import time

OP_HANDSHAKE = 0
OP_FRAME = 1
OP_CLOSE = 2

TRY_RECONNECTING = True

### Logger ###
log = logging.getLogger("Discord RPC")
log.setLevel(logging.INFO)
logging.basicConfig(format="%(asctime)s :: [%(levelname)s @ %(filename)s.%(funcName)s:%(lineno)d] :: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")


class RPC:
    def __init__(self, app_id:int, debug:bool=False, output:bool=True, exit_if_discord_close:bool=True, exit_on_disconnect:bool=True):
        self.app_id = str(app_id)
        self.exit_if_discord_close = exit_if_discord_close
        self.exit_on_disconnect = exit_on_disconnect

        self.user_data = {}
        self.User = User()

        if debug == True:
            log.setLevel(logging.DEBUG)
        
        if output == False:
            log.disabled = True

        self.is_running = False
        self._setup()

    def _setup(self):
        if sys.platform == "win32":
            self.ipc = WindowsPipe(self.app_id, self.exit_if_discord_close, self.exit_on_disconnect)
        else:
            self.ipc = UnixPipe(self.app_id, self.exit_if_discord_close, self.exit_on_disconnect)
            
        if not self.ipc.connected: return
        self.user_data = self.ipc.handshake()
        self.User = User(self.user_data)
    
    def set_activity(
            self,
            state: str=None, details:str=None, act_type:Activity=Activity.Playing,
            state_url:str=None, details_url:str=None,
            ts_start:int=None, ts_end:int=None,
            progressbar:dict=None,
            use_local_time:bool=False,
            large_image:str=None, large_text:str=None,
            small_image:str=None, small_text:str=None,
            party_id:str=None, party_size:list=None,
            join_secret:str=None, spectate_secret:str=None,
            match_secret:str=None, buttons:list=None,
            clear=False
        ) -> bool:

        if type(party_id) == int:
            party_id = str(party_id)

        if type(act_type) != Activity:
            raise InvalidActivityType(type(act_type))

        # https://github.com/Senophyx/Discord-RPC/issues/28#issuecomment-2301287350
        if act_type in [Activity.Streaming, Activity.Custom]:
            raise ActivityTypeDisabled()

        if buttons and len(buttons) > 2:
            raise ButtonError("Max 2 buttons allowed")

        if progressbar:
            act_type = Activity.Listening
            ts_start = progressbar["ts_start"]
            ts_end = progressbar["ts_end"]

        elif use_local_time:
            ts_start = ts_start_as_local_time()
            ts_end = None
            
        act = {
            "state": state,
            "details": details,
            "type": act_type.value,
            "state_url": state_url,
            "details_url": details_url,
            "timestamps": {
                "start": ts_start,
                "end": ts_end
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
                'activity': None if clear else remove_none(act)
            },
            'nonce': str(uuid.uuid4())
        }

        if not self.ipc.connected and TRY_RECONNECTING:
            self._setup()

        if not self.ipc.connected:
            return

        try:
            self.ipc._send(payload, OP_FRAME)
            self.is_running = True
            log.info('RPC set')
            return True
        except Exception as e:
            log.error('Failed to set RPC')
            self.disconnect()

    def clear(self):
        self.set_activity(clear=True)

    def disconnect(self):
        if not self.ipc.connected:
            return

        self.ipc.disconnect()
        self.is_running = False

    def run(self, update_every:int=1):
        try:
            while True:
                time.sleep(update_every)
        except KeyboardInterrupt:
            self.disconnect()

class WindowsPipe:
    def __init__(self, app_id, exit_if_discord_close, exit_on_disconnect):
        self.app_id = app_id
        self.exit_if_discord_close = exit_if_discord_close
        self.exit_on_disconnect = exit_on_disconnect
        self.connected = True

        base_path = R'\\?\pipe\discord-ipc-{}'
        
        for i in range(10):
            path = base_path.format(i)

            try:
                self.socket = open(path, "w+b")
            except OSError as e:
                if self.exit_if_discord_close:
                    log.debug("Failed to open {!r}: {}".format(path, e))
                    raise DiscordNotOpened()
                else:
                    log.debug("Discord seems to be close.")
            else:
                break

        else:
            if self.exit_if_discord_close:
                raise DiscordNotOpened()
            else:
                log.warning("Discord is closed")
                self.connected = False

        if self.connected:
            log.debug(f"Connected to {path}")

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

        log.debug(output)
        return output

    def _send(self, payload, op=OP_FRAME):
        log.debug(payload)

        payload = json.dumps(payload).encode('UTF-8')
        payload = struct.pack('<ii', op, len(payload)) + payload

        self.socket.write(payload)
        self.socket.flush()

    def handshake(self):
        self._send({'v': 1, 'client_id': self.app_id}, op=OP_HANDSHAKE)
        data = self._recv()

        try:
            if data['cmd'] == 'DISPATCH' and data['evt'] == 'READY':
                log.info(f"Connected to {data['data']['user']['username']} ({data['data']['user']['id']})")
                return data['data']['user']
            
            else:
                raise RPCException()

        except KeyError:
            if data['code'] == 4000:
                raise InvalidID()

    def disconnect(self):
        try:
            self._send({}, OP_CLOSE)
            self.socket.close()
        except Exception as e:
            log.debug("Socket closed before command was received")

        self.socket = None
        self.connected = False

        log.warning("Closing RPC")
        if self.exit_on_disconnect:
            sys.exit()

class UnixPipe:
    def __init__(self, app_id, exit_if_discord_close, exit_on_disconnect):
        self.app_id = app_id
        self.exit_if_discord_close = exit_if_discord_close
        self.exit_on_disconnect = exit_on_disconnect
        self.connected = True

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
            if self.exit_if_discord_close:
                raise DiscordNotOpened()
            else:
                log.warning("Discord is closed")
                self.connected = False

        if self.connected:
            log.debug(f"Connected to {path}")


    def _recv(self):
        recv_data = self.socket.recv(1024)
        enc_header = recv_data[:8]
        dec_header = struct.unpack("<ii", enc_header)
        enc_data = recv_data[8:]

        output = json.loads(enc_data.decode('UTF-8'))
        
        log.debug(output)
        return output
    
    def _send(self, payload, op=OP_FRAME):
        log.debug(payload)

        payload = json.dumps(payload).encode('UTF-8')
        payload = struct.pack('<ii', op, len(payload)) + payload

        self.socket.send(payload)
    
    def handshake(self):
        self._send({'v': 1, 'client_id': self.app_id}, op=OP_HANDSHAKE)
        data = self._recv()

        try:
            if data['cmd'] == 'DISPATCH' and data['evt'] == 'READY':
                log.info(f"Connected to {data['data']['user']['username']} ({data['data']['user']['id']})")
                return data['data']['user']
            
            else:
                raise RPCException()

        except KeyError:
            if data['code'] == 4000:
                raise InvalidID()
    
    def disconnect(self):
        try:
            self._send({}, OP_CLOSE)
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except Exception as e:
            log.debug("Socket closed before command was received")

        self.socket = None
        self.connected = False

        log.warning("Closing RPC")
        if self.exit_on_disconnect:
            sys.exit()
