import json
import struct
import threading
import time
import unittest

from discordrpc.presence import _BasePipe, OP_FRAME, OP_PING, OP_PONG


class FakePipe(_BasePipe):
    def __init__(self):
        super().__init__(None, False, False)
        self._in = queue.Queue()
        self._out = queue.Queue()
        self._buffer = b""
        self.connected = True

    def _connect_pipe(self):
        return True

    def _write(self, data):
        self._out.put(data)

    def _read_some(self, size):
        if self._buffer:
            chunk = self._buffer[:size]
            self._buffer = self._buffer[size:]
            return chunk
        while True:
            try:
                data = self._in.get(timeout=0.1)
            except queue.Empty:
                if self._reader_stop.is_set():
                    return b""
                continue
            if len(data) <= size:
                return data
            self._buffer = data[size:]
            return data[:size]

    def _close(self):
        pass


def build_frame(opcode, payload):
    data = json.dumps(payload).encode("UTF-8")
    return struct.pack("<ii", opcode, len(data)) + data


class HeartbeatTests(unittest.TestCase):
    def test_incoming_ping_is_answered_with_pong(self):
        pipe = FakePipe()
        pipe._start_reader()
        pipe._in.put(build_frame(OP_PING, {"v": 1}))

        deadline = time.time() + 2
        while time.time() < deadline and pipe._out.empty():
            time.sleep(0.05)

        self.assertFalse(pipe._out.empty())
        frame = pipe._out.get()
        opcode, length = struct.unpack("<ii", frame[:8])
        self.assertEqual(opcode, OP_PONG)
        self.assertEqual(length, len(frame) - 8)
        pipe.disconnect()

    def test_pong_does_not_corrupt_next_request(self):
        pipe = FakePipe()
        pipe._start_reader()
        # Inject a PONG before the real response.
        pipe._in.put(build_frame(OP_PONG, {"v": 1}))
        resp = {"cmd": "SET_ACTIVITY", "nonce": "n1", "data": {"x": 1}}
        pipe._in.put(build_frame(OP_FRAME, resp))

        result = pipe._request({"cmd": "SET_ACTIVITY", "nonce": "n1"}, timeout=2)
        self.assertTrue(result.get("ok"))
        self.assertEqual(result.get("data"), {"x": 1})
        pipe.disconnect()


import queue

if __name__ == "__main__":
    unittest.main(verbosity=2)
