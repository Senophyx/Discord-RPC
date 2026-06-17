import sys
import os
import socket
import json
import struct
import uuid
from typing import Optional
from .exceptions import (
    RPCException, InvalidID, DiscordNotOpened,
    ButtonError, InvalidActivityType, ActivityTypeDisabled,
)
from .types import Activity, StatusDisplay, User, Application
from .utils import remove_none, get_app_info
import logging
import time

OP_HANDSHAKE = 0
OP_FRAME = 1
OP_CLOSE = 2
OP_PING = 3
OP_PONG = 4

### Logger ###
log = logging.getLogger("Discord RPC")
log.setLevel(logging.INFO)
log.addHandler(logging.NullHandler())

# Guard: only add the output handler once across all RPC instances
_log_output_handler_added = False


class RPC:
    def __init__(self, app_id:int, debug:bool=False, output:bool=True, exit_if_discord_close:bool=True, exit_on_disconnect:bool=True):
        self.app_id = str(app_id)
        self.exit_if_discord_close = exit_if_discord_close
        self.exit_on_disconnect = exit_on_disconnect

        self.try_reconnecting = True
        self.User = User()
        
        self.App = None

        if debug == True:
            log.setLevel(logging.DEBUG)
        
        if output and not _log_output_handler_added:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s :: [%(levelname)s @ %(filename)s.%(funcName)s:%(lineno)d] :: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
            handler.setFormatter(formatter)
            log.addHandler(handler)
            global _log_output_handler_added
            _log_output_handler_added = True
        elif not output:
            log.disabled = True

        self.is_running = False
        self._setup()

    def _setup(self):
        if sys.platform == "win32":
            self.ipc = WindowsPipe(self.app_id, self.exit_if_discord_close, self.exit_on_disconnect)
        else:
            self.ipc = UnixPipe(self.app_id, self.exit_if_discord_close, self.exit_on_disconnect)
            
        if not self.ipc.connected: return
        user_data = self.ipc.handshake()
        self.User = User(user_data)
    
    def get_app_info(self):
        if not self.App:
            app_info = get_app_info(self.app_id)
            self.App = Application(app_info)
        return self.App

    def set_activity(
            self,
            state: str=None, details:str=None, act_type:Activity=Activity.Playing, status_type:StatusDisplay=StatusDisplay.Name,
            large_image:str=None, large_text:str=None, large_url:str=None,
            small_image:str=None, small_text:str=None, small_url:str=None,
            state_url:str=None, details_url:str=None,
            ts_start:int=None, ts_end:int=None,
            party_id:str=None, party_size:list=None,
            join_secret:str=None, spectate_secret:str=None,
            match_secret:str=None, buttons:list=None,
            clear=False
        ) -> Optional[bool]:
        """
        Set or update the Rich Presence.
        
        Images (`large_image`, `small_image`) can be an uploaded asset key from your Discord Developer Portal, 
        or an external direct URL (e.g., https://example.com/image.gif). Supports PNG, JPEG, WebP, GIF, and AVIF.
        """

        if type(act_type) != Activity:
            raise InvalidActivityType(type(act_type))

        # https://github.com/Senophyx/Discord-RPC/issues/28#issuecomment-2301287350
        if act_type in [Activity.Streaming, Activity.Custom]:
            raise ActivityTypeDisabled()

        if buttons and len(buttons) > 2:
            raise ButtonError("Max 2 buttons allowed")

        activity = None
        if not clear:
            if type(party_id) == int:
                party_id = str(party_id)

            act = {
                "state": state,
                "details": details,
                "type": act_type.value,
                "status_display_type": status_type.value,
                "state_url": state_url,
                "details_url": details_url,
                "timestamps": {
                    "start": ts_start,
                    "end": ts_end
                },
                "assets": {
                    "large_image": large_image,
                    "large_text": large_text,
                    "large_url": large_url,
                    "small_image": small_image,
                    "small_text": small_text,
                    "small_url": small_url
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
            activity = remove_none(act)

        payload = {
            'cmd': 'SET_ACTIVITY',
            'args': {
                'pid': os.getpid(),
                'activity': activity
            },
            'nonce': str(uuid.uuid4())
        }

        if not self.ipc.connected and self.try_reconnecting:
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

    def run(self, update_every:int=1, ping_every:int=15):
        try:
            last_ping = time.time()
            while True:
                time.sleep(update_every)
                
                # Send a PING heartbeat every `ping_every` seconds to keep the socket alive
                if self.ipc.connected and (time.time() - last_ping >= ping_every):
                    payload = {"v": 1, "client_id": self.app_id}
                    try:
                        self.ipc._send(payload, OP_PING)
                        last_ping = time.time()
                    except Exception as e:
                        log.debug(f"Heartbeat PING failed: {e}")
                        self.disconnect()
        except KeyboardInterrupt:
            self.disconnect()


class _BasePipe:
    def __init__(self, app_id, exit_if_discord_close, exit_on_disconnect):
        self.app_id = app_id
        self.exit_if_discord_close = exit_if_discord_close
        self.exit_on_disconnect = exit_on_disconnect
        self.connected = self._connect_pipe()

    def _connect_pipe(self):
        """Override in subclass to establish the pipe connection. Returns True on success."""
        raise NotImplementedError

    def _send(self, payload, op=OP_FRAME):
        log.debug(payload)

        payload = json.dumps(payload).encode('UTF-8')
        payload = struct.pack('<ii', op, len(payload)) + payload

        self._write(payload)

    def _write(self, data: bytes):
        """Override in subclass to write bytes to the pipe."""
        raise NotImplementedError

    def _recv(self):
        """Override in subclass to receive data from the pipe."""
        raise NotImplementedError

    def handshake(self):
        self._send({'v': 1, 'client_id': self.app_id}, op=OP_HANDSHAKE)
        data = self._recv()

        if data.get('cmd') == 'DISPATCH' and data.get('evt') == 'READY':
            user = data.get('data', {}).get('user')
            if user:
                log.info(f"Connected to {user.get('username')} ({user.get('id')})")
                return user

        if data.get('code') == 4000:
            raise InvalidID()

        raise RPCException()

    def disconnect(self):
        try:
            self._send({}, OP_CLOSE)
            self._close()
        except Exception as e:
            log.debug("Socket closed before command was received")

        self.socket = None
        self.connected = False

        log.warning("Closing RPC")
        if self.exit_on_disconnect:
            sys.exit()

    def _close(self):
        """Override in subclass to close the socket."""
        raise NotImplementedError


class WindowsPipe(_BasePipe):
    def _connect_pipe(self):
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
            return False

        log.debug(f"Connected to {path}")
        return True

    def _write(self, data: bytes):
        self.socket.write(data)
        self.socket.flush()

    def _close(self):
        self.socket.close()

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


class UnixPipe(_BasePipe):
    def _connect_pipe(self):
        self.socket = socket.socket(socket.AF_UNIX)

        raw_path = (
            os.environ.get('XDG_RUNTIME_DIR')
            or os.environ.get('TMPDIR')
            or os.environ.get('TMP')
            or os.environ.get('TEMP')
            or '/tmp'
        ).rstrip('/')
        base_path = raw_path + '/discord-ipc-{0}'

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
            return False

        log.debug(f"Connected to {path}")
        return True

    def _write(self, data: bytes):
        self.socket.send(data)

    def _close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def _recv(self):
        enc_header = b''
        header_size = 8

        while header_size:
            chunk = self.socket.recv(header_size)
            if not chunk:
                break
            enc_header += chunk
            header_size -= len(chunk)

        dec_header = struct.unpack("<ii", enc_header)
        enc_data = b''
        remain_packet_size = int(dec_header[1])

        while remain_packet_size:
            chunk = self.socket.recv(remain_packet_size)
            if not chunk:
                break
            enc_data += chunk
            remain_packet_size -= len(chunk)

        output = json.loads(enc_data.decode('UTF-8'))

        log.debug(output)
        return output
