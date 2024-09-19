import sys
import os
import time
import uuid
import logging
import asyncio
from typing import Union

from .exceptions import *
from .pipe import WindowsPipe, UnixPipe, Handshake
from .utils import remove_none

_log = logging.getLogger(__name__)


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
        self.User = {}

        if not output:
            _log.disabled = True

        self.is_running = False
        self._setup()

    def _setup(self):
        if sys.platform == "win32":
            self.ipc = WindowsPipe(self.app_id, self.exit_if_discord_close)
            if not self.ipc.connected:
                return

            self.User = self.ipc.handshake()

        else:
            self.ipc = UnixPipe(self.app_id, self.exit_if_discord_close)
            if not self.ipc.connected:
                return

            self.User = self.ipc.handshake()

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
        _log.info('RPC set')

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
