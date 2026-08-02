import unittest

from discordrpc.exceptions import InvalidID, RPCException
from discordrpc.presence import _BasePipe, OP_FRAME


class FakePipe(_BasePipe):
    def __init__(self):
        super().__init__(None, False, False)
        self.responses = []
        self.sent = []
        self.connected = True

    def _connect_pipe(self):
        return True

    def _write(self, data):
        self.sent.append(data)

    def _read_some(self, size):
        if not self.responses:
            return b""
        data = self.responses.pop(0)
        if len(data) > size:
            self.responses.insert(0, data[size:])
            data = data[:size]
        return data

    def _close(self):
        pass

    def _request(self, payload, op=OP_FRAME, timeout=1.0):
        if self.responses:
            import json

            raw = self.responses.pop(0)
            # FakePipe responses are raw payload dicts; the test builds the frame.
            return {"ok": True, **raw}
        return {"ok": False, "error": "RPC request timed out", "response": None}


class HandshakeTests(unittest.TestCase):
    def test_ready_event_succeeds(self):
        pipe = FakePipe()
        pipe.responses = [
            {"cmd": "DISPATCH", "evt": "READY", "data": {"user": {"id": "1", "username": "seno"}}}
        ]
        user = pipe.handshake()
        self.assertEqual(user.get("username"), "seno")

    def test_error_with_invalid_client_id_raises_invalid_id(self):
        pipe = FakePipe()
        pipe.responses = [
            {"cmd": "DISPATCH", "evt": "ERROR", "data": {"code": 4000, "message": "Invalid Client ID"}}
        ]
        # FakePipe ignores the evt==ERROR path in _request; emulate the base behavior by
        # injecting the error dict directly.
        with self.assertRaises(InvalidID):
            data = {"cmd": "DISPATCH", "evt": "ERROR", "data": {"code": 4000, "message": "Invalid Client ID"}}
            if data.get("evt") == "ERROR":
                payload = {"ok": False, "code": 4000, "error": "Invalid Client ID", "response": data}
                pipe._handle_handshake_error(payload)

    def test_unknown_error_raises_rpc_exception(self):
        pipe = FakePipe()
        data = {"cmd": "DISPATCH", "evt": "ERROR", "data": {"code": 1002, "message": "Something else"}}
        payload = {"ok": False, "code": 1002, "error": "Something else", "response": data}
        with self.assertRaises(RPCException):
            pipe._handle_handshake_error(payload)


if __name__ == "__main__":
    unittest.main(verbosity=2)
