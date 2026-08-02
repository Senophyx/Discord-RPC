import queue
import threading
import time
import unittest

from discordrpc.presence import _BasePipe, OP_FRAME, OP_CLOSE, OP_PING


class FakePipe(_BasePipe):
    """Synchronous fake transport whose socket is driven by an in-process byte queue."""

    def __init__(self):
        super().__init__(None, False, False)
        self._in = queue.Queue()
        self._out = queue.Queue()
        self.connected = True
        self._close_called = False

    def _connect_pipe(self):
        return True

    def _write(self, data):
        self._out.put(data)

    def _read_some(self, size):
        try:
            data = self._in.get(timeout=0.1)
        except queue.Empty:
            return b""
        if len(data) > size:
            self._in.put(data[size:])
            data = data[:size]
        return data

    def _close(self):
        self._close_called = True


def build_frame(opcode, payload):
    import json
    import struct

    data = json.dumps(payload).encode("UTF-8")
    return struct.pack("<ii", opcode, len(data)) + data


class RequestRoutingTests(unittest.TestCase):
    def test_request_routes_by_nonce(self):
        pipe = FakePipe()
        pipe._start_reader()
        payload = {"cmd": "SET_ACTIVITY", "nonce": "n1"}
        result = pipe._request(payload, timeout=1)

        # FakePipe never sends a response, so the request should time out quickly.
        self.assertFalse(result.get("ok"))
        self.assertEqual(result.get("error"), "RPC request timed out")
        pipe.disconnect()

    def test_response_with_matching_nonce_succeeds(self):
        pipe = FakePipe()
        pipe._start_reader()
        payload = {"cmd": "SET_ACTIVITY", "nonce": "n1"}
        resp = {"cmd": "SET_ACTIVITY", "nonce": "n1", "data": {"x": 1}}

        # Inject the response as if Discord sent it.
        pipe._in.put(build_frame(OP_FRAME, resp))
        result = pipe._request(payload, timeout=2)
        self.assertTrue(result.get("ok"))
        self.assertEqual(result.get("data"), {"x": 1})
        pipe.disconnect()

    def test_response_with_mismatched_nonce_is_rejected(self):
        pipe = FakePipe()
        pipe._start_reader()
        payload = {"cmd": "SET_ACTIVITY", "nonce": "n1"}
        resp = {"cmd": "SET_ACTIVITY", "nonce": "n2", "data": {"x": 1}}

        pipe._in.put(build_frame(OP_FRAME, resp))
        result = pipe._request(payload, timeout=1)
        self.assertFalse(result.get("ok"))
        pipe.disconnect()

    def test_pong_is_not_treated_as_command_response(self):
        pipe = FakePipe()
        pipe._start_reader()
        payload = {"cmd": "SET_ACTIVITY", "nonce": "n1"}
        pong = {"cmd": "PONG", "nonce": "n1"}

        pipe._in.put(build_frame(4, pong))
        result = pipe._request(payload, timeout=1)
        self.assertFalse(result.get("ok"))
        pipe.disconnect()

    def test_error_response_preserves_code_and_message(self):
        pipe = FakePipe()
        pipe._start_reader()
        payload = {"cmd": "SET_ACTIVITY", "nonce": "n1"}
        error_resp = {"cmd": "SET_ACTIVITY", "nonce": "n1", "evt": "ERROR", "data": {"code": 4007, "message": "Invalid Client ID"}}

        pipe._in.put(build_frame(OP_FRAME, error_resp))
        result = pipe._request(payload, timeout=2)
        self.assertFalse(result.get("ok"))
        self.assertEqual(result.get("code"), 4007)
        self.assertEqual(result.get("error"), "Invalid Client ID")
        pipe.disconnect()


class WriteSerializationTests(unittest.TestCase):
    def test_concurrent_writes_do_not_interleave(self):
        pipe = FakePipe()
        frames = []

        def writer(n):
            for _ in range(50):
                pipe._send({"cmd": "X", "nonce": f"n{n}"})

        threads = [threading.Thread(target=writer, args=(i,)) for i in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=5)

        # Every frame must parse cleanly as header+json payload.
        for frame in list(pipe._out.queue):
            header = frame[:8]
            import struct

            opcode, length = struct.unpack("<ii", header)
            self.assertEqual(opcode, OP_FRAME)
            self.assertEqual(length, len(frame) - 8)
            import json

            payload = json.loads(frame[8:].decode("UTF-8"))
            self.assertIn("nonce", payload)
        pipe.disconnect()


if __name__ == "__main__":
    unittest.main(verbosity=2)
