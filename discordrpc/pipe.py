import enum
import json
import logging
import os
import re
import socket
import struct
import sys

from .exceptions import InvalidID, RPCException, DiscordNotOpened, Error

_log = logging.getLogger(__name__)


class Handshake(enum.IntEnum):
    OP_HANDSHAKE = 0
    OP_FRAME = 1
    OP_CLOSE = 2


def check_discord_close(exit_if_discord_close: bool) -> bool:
    if not exit_if_discord_close:
        raise DiscordNotOpened()
    _log.debug("Discord seems to be close.")
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

        _log.debug(output)
        return output

    def _send(self, payload, op=Handshake.OP_FRAME):
        _log.debug(payload)

        payload = json.dumps(payload).encode('UTF-8')
        payload = struct.pack('<ii', op, len(payload)) + payload

        self.socket.write(payload)
        self.socket.flush()

    def handshake(self):
        self._send({'v': 1, 'client_id': self.app_id}, op=Handshake.OP_HANDSHAKE)
        data = self._recv()
        if data.get('cmd') == 'DISPATCH' and data.get('evt') == 'READY':
            user = data.get('data', {}).get('user', {})
            _log.info("Connected to %s (%s)", user.get('username'), user.get('id'))
            return True
        if data.get('code', 4000) == 4000:
            raise InvalidID
        raise RPCException()

    def disconnect(self):
        self._send({}, Handshake.OP_CLOSE)

        if self.socket is not None:
            self.socket.close()
        self.socket = None

        _log.warning("Closing RPC")
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
            _log.debug("Connected to %s", path)


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
            _log.debug("Connected to %s", path)

    def _recv(self):
        recv_data = self.socket.recv(1024)
        enc_header = recv_data[:8]
        _ = struct.unpack("<ii", enc_header)
        enc_data = recv_data[8:]

        output = json.loads(enc_data.decode('UTF-8'))

        _log.debug(output)
