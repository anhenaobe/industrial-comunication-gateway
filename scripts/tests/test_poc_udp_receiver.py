"""Receiver behavior tests, including one real IPv4 loopback datagram."""

import contextlib
import importlib.util
import io
from pathlib import Path
import socket
import threading
import time
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "receiver", Path(__file__).resolve().parents[1] / "poc_udp_receiver.py"
)
receiver = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(receiver)


class ReceiverTest(unittest.TestCase):
    def test_loopback_datagram_and_interrupt_close(self):
        real_socket = socket.socket
        received = threading.Event()
        host_socket = real_socket(socket.AF_INET, socket.SOCK_DGRAM)
        host_socket.bind(("127.0.0.1", 0))
        port = host_socket.getsockname()[1]
        deadline = time.monotonic() + 3.0

        class OnePacket:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                host_socket.close()

            def bind(self, address):
                pass  # already bound to the OS-assigned port

            def settimeout(self, timeout):
                host_socket.settimeout(timeout)

            def recvfrom(self, size):
                if received.is_set():
                    raise KeyboardInterrupt
                if time.monotonic() >= deadline:
                    raise AssertionError("Loopback datagram not received within 3 seconds")
                result = host_socket.recvfrom(size)
                received.set()
                return result

        def send():
            with real_socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
                sender.sendto(b"poc=gateway seq=7 uptime_ms=123\n", ("127.0.0.1", port))

        output = io.StringIO()
        sender = threading.Thread(target=send)
        sender.start()
        try:
            with patch.object(receiver.socket, "socket", return_value=OnePacket()), \
                    patch("sys.argv", ["receiver", "--port", str(port)]), \
                    contextlib.redirect_stdout(output):
                receiver.main()
        finally:
            sender.join(timeout=2)
            host_socket.close()
        self.assertTrue(received.is_set())
        self.assertIn("127.0.0.1:", output.getvalue())
        self.assertIn("seq=7", output.getvalue())
        self.assertIn("Receiver stopped", output.getvalue())
        self.assertEqual(host_socket.fileno(), -1)

    def test_arbitrary_text_and_terminal_controls(self):
        fake = unittest.mock.MagicMock()
        fake.__enter__.return_value = fake
        fake.recvfrom.side_effect = [
            (b"no sequence\x1b[2J\xff", ("127.0.0.1", 12345)), KeyboardInterrupt
        ]
        output = io.StringIO()
        with patch.object(receiver.socket, "socket", return_value=fake), \
                patch("sys.argv", ["receiver"]), contextlib.redirect_stdout(output):
            receiver.main()
        self.assertIn("seq=unavailable", output.getvalue())
        self.assertNotIn("\x1b", output.getvalue())
        self.assertIn(r"\x1b", output.getvalue())

    def test_invalid_port(self):
        with patch("sys.argv", ["receiver", "--port", "65536"]), \
                contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            receiver.main()
        self.assertEqual(error.exception.code, 2)

    def test_bind_error_is_reported(self):
        fake = unittest.mock.MagicMock()
        fake.__enter__.return_value = fake
        fake.bind.side_effect = OSError("address unavailable")
        output = io.StringIO()
        with patch.object(receiver.socket, "socket", return_value=fake), \
                patch("sys.argv", ["receiver"]), contextlib.redirect_stderr(output), \
                self.assertRaises(SystemExit) as error:
            receiver.main()
        self.assertEqual(error.exception.code, 1)
        self.assertIn("address unavailable", output.getvalue())


if __name__ == "__main__":
    unittest.main()
