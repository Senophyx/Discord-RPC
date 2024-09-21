import enum
import json
import re
import socket
import struct
import sys
import os
import time
import uuid
import logging
import asyncio
from typing import Union

from .exceptions import *
from .utils import remove_none

log = logging.getLogger(__name__)


class RPC:
    def __init__(
            self,
            app_id: int,
            output: bool = True,
            exit_if_discord_close: bool = True,
            reconnection: bool = True
    ):
        self.app_id = str(app_id)
        self.reconnection = reconnection
        self.exit_if_discord_close = exit_if_discord_close
        self.User={}

        if not output:
            log.disabled = True

        self.is_running = False
        self._setup()

    def _setup(self):
        if sys.platform == "win32":
            self.ipc = WindowsPipe(self.app_id, self.exit_if_discord_close)
            if not self.ipc.connected:
                return

            self.User=self.ipc.handshake()

        else:
            self.ipc = UnixPipe(self.app_id, self.exit_if_discord_close)
            if not self.ipc.connected:
                return

            self.User=self.ipc.handshake()
    
    def set_activity(
            self,
            state: str = None,
            details: str = None,
            act_type: int = 0,
            ts_start: int = None,
            ts_end: int = None,
            large_image: str = None,
            large_text: str = None,
            small_image: str = None,
            small_text: str = None,
            party_id: Union[str, int] = None,
            party_size: list = None,
            join_secret: str = None,
            spectate_secret: str = None,
            match_secret: str = None,
            buttons: list[dict] = None
    ):

        if isinstance(party_id, int):
            party_id = str(party_id)

        if buttons is not None and not isinstance(buttons, list):
            raise TypeError("the buttons must be a class of Buttons")

        # https://github.com/Senophyx/Discord-RPC/issues/28#issuecomment-2301287350
        if any(inv_type in str(act_type) for inv_type in ["1", "4"]):
            raise InvalidActivityType()

        act = {
            "state": state,
            "details": details,
            "type": act_type,
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
                'activity': remove_none(act)
            },
            'nonce': str(uuid.uuid4())
        }

        if not self.ipc.connected and self.reconnection:
            self._setup()

        if not self.ipc.connected:
            return

        self.ipc._send(payload, Handshake.OP_FRAME)
        self.is_running = True
        log.info('RPC set')

    def disconnect(self):
        if not self.ipc.connected:
            return

        self.ipc.disconnect()
        self.is_running = False

    def run(self, update_every: int = 1):
        try:
            while True:
                time.sleep(update_every)
        except KeyboardInterrupt:
            self.disconnect()

    async def run_async(self, update_every: int = 1):
        try:
            while True:
                await asyncio.sleep(update_every)
        except KeyboardInterrupt:
            self.disconnect()


class Handshake(enum.IntEnum):
    OP_HANDSHAKE = 0
    OP_FRAME = 1
    OP_CLOSE = 2


def check_discord_close(exit_if_discord_close: bool) -> bool:
    if not exit_if_discord_close:
        raise DiscordNotOpened()
    log.debug("Discord seems to be close.")
    return False


class BasePipe:
    def __init__(self, app_id: str):
        self.app_id = app_id
        self.connected = True
        self.socket = None

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

    def _send(self, payload, op=Handshake.OP_FRAME):
        log.debug(payload)

        payload = json.dumps(payload).encode('UTF-8')
        payload = struct.pack('<ii', op, len(payload)) + payload

        self.socket.write(payload)
        self.socket.flush()

    def handshake(self):
        self._send({'v': 1, 'client_id': self.app_id}, op=Handshake.OP_HANDSHAKE)
        data = self._recv()
        try:
            if data['cmd'] == 'DISPATCH' and data['evt'] == 'READY':
                log.info(f"Connected to {data['data']['user']['username']} ({data['data']['user']['id']})")
                return data['data']['user']
            
            else:
                raise RPCException()

        except KeyError:
            if data['code'] == 4000:
                raise InvalidID

    def disconnect(self):
        self._send({}, Handshake.OP_CLOSE)

        if self.socket is not None:
            self.socket.close()
        self.socket = None

        log.warning("Closing RPC")
        sys.exit()


class WindowsPipe(BasePipe):
    def __init__(self, app_id: str, exit_if_discord_close: bool):
        super().__init__(app_id)
        base_path = R'\\?\pipe\discord-ipc-{}'
        path = ""

        for i in range(10):
            path = base_path.format(i)
            try:
                self.socket = open(path, "w+b")
            except OSError as e:
                if not exit_if_discord_close:
                    raise Error(f"Failed to open {path!r}: {e}")
            else:
                break

        else:
            self.connected = check_discord_close(exit_if_discord_close)

        if self.connected:
            log.debug("Connected to %s", path)


class UnixPipe(BasePipe):
    def __init__(self, app_id: str, exit_if_discord_close: bool):
        super().__init__(app_id)
        self.socket = socket.socket(socket.AF_UNIX)

        path = (
                os.environ.get('XDG_RUNTIME_DIR') or os.environ.get('TMPDIR') or
                os.environ.get('TMP') or os.environ.get('TEMP') or '/tmp')
        base_path = re.sub(r'\\/$', '', path) + '/discord-ipc-{0}'

        for i in range(10):
            path = base_path.format(i)

            try:
                self.socket.connect(path)
                break
            except FileNotFoundError:
                pass

        else:
            self.connected = check_discord_close(exit_if_discord_close)

        if self.connected:
            log.debug("Connected to %s", path)

    def _recv(self):
        recv_data = self.socket.recv(1024)
        enc_header = recv_data[:8]
        _ = struct.unpack("<ii", enc_header)
        enc_data = recv_data[8:]

        output = json.loads(enc_data.decode('UTF-8'))

        log.debug(output)
        return output

    def _send(self, payload, op=Handshake.OP_FRAME):
        log.debug(payload)

        payload = json.dumps(payload).encode('UTF-8')
        payload = struct.pack('<ii', op, len(payload)) + payload

        self.socket.write(payload)
        self.socket.flush()

    def handshake(self):
        self._send({'v': 1, 'client_id': self.app_id}, op=Handshake.OP_HANDSHAKE)
        data = self._recv()
        try:
            if data['cmd'] == 'DISPATCH' and data['evt'] == 'READY':
                log.info(f"Connected to {data['data']['user']['username']} ({data['data']['user']['id']})")
                return data['data']['user']
            
            else:
                raise RPCException()

        except KeyError:
            if data['code'] == 4000:
                raise InvalidID
