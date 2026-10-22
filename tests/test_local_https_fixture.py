"""Local-only HTTPS integration tests; never contact an external host."""
import http.client
import shutil
import socket
import ssl
import subprocess
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class _FixtureHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        if self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/ok")
            self.end_headers()
            return
        if self.path == "/slow":
            time.sleep(0.35)
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()

    def log_message(self, *_args):
        pass


class LocalHTTPSFixtureTests(unittest.TestCase):
    """Exercise TLS and HTTP edge cases against a loopback-only fixture."""

    @classmethod
    def setUpClass(cls):
        if not shutil.which("openssl"):
            raise unittest.SkipTest("OpenSSL CLI is required to create a temporary test certificate")
        cls._temp = tempfile.TemporaryDirectory(prefix="syn-launch-local-https-")
        root = Path(cls._temp.name)
        cls.cert = root / "cert.pem"
        key = root / "key.pem"
        subprocess.run(
            ["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
             "-keyout", str(key), "-out", str(cls.cert), "-days", "1",
             "-subj", "/CN=localhost", "-addext", "subjectAltName=DNS:localhost,IP:127.0.0.1"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20,
        )
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), _FixtureHandler)
        server_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        server_context.load_cert_chain(str(cls.cert), str(key))
        cls.server.socket = server_context.wrap_socket(cls.server.socket, server_side=True)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.port = cls.server.server_address[1]

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "server"):
            cls.server.shutdown()
            cls.server.server_close()
            cls.thread.join(timeout=2)
        if hasattr(cls, "_temp"):
            cls._temp.cleanup()

    def _request(self, context, path="/ok", timeout=2):
        conn = http.client.HTTPSConnection("localhost", self.port, context=context, timeout=timeout)
        try:
            conn.request("HEAD", path)
            return conn.getresponse()
        except BaseException:
            conn.close()
            raise

    def test_trusted_temporary_certificate_succeeds(self):
        context = ssl.create_default_context(cafile=str(self.cert))
        response = self._request(context)
        try:
            self.assertEqual(response.status, 200)
        finally:
            response.read()

    def test_untrusted_certificate_is_rejected(self):
        context = ssl.create_default_context()
        with self.assertRaises(ssl.SSLCertVerificationError):
            self._request(context)

    def test_redirect_is_returned_without_following(self):
        context = ssl.create_default_context(cafile=str(self.cert))
        response = self._request(context, "/redirect")
        try:
            self.assertEqual(response.status, 302)
            self.assertEqual(response.getheader("Location"), "/ok")
        finally:
            response.read()

    def test_socket_timeout_is_enforced(self):
        context = ssl.create_default_context(cafile=str(self.cert))
        started = time.monotonic()
        with self.assertRaises((TimeoutError, socket.timeout)):
            self._request(context, "/slow", timeout=0.08)
        self.assertLess(time.monotonic() - started, 0.30)

    def test_production_adapter_rejects_local_custom_port_before_network(self):
        from workflow_adapters import run_web_api_review
        with self.assertRaises(ValueError):
            run_web_api_review(f"https://localhost:{self.port}/ok")


if __name__ == "__main__":
    unittest.main()
