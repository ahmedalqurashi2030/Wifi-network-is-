#!/usr/bin/env python3
"""Controlled localhost-only target for the Ethical Hacking coursework lab.

This service intentionally exposes benign training misconfigurations so scanners
can produce meaningful results. It binds only to 127.0.0.1.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import threading

HOST = "127.0.0.1"
HTTP_PORT = 8080
BANNER_PORT = 2222


class LabHandler(BaseHTTPRequestHandler):
    server_version = "Apache/2.2.8"
    sys_version = "(Ubuntu) DAV/2"

    def _headers(self, status=200, content_type="text/html; charset=utf-8", length=None):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("X-Powered-By", "PHP/5.2.4-2ubuntu5.10")
        # Intentionally omit modern security headers for vulnerability-scanner evidence.
        if length is not None:
            self.send_header("Content-Length", str(length))
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            body = b"""<html><head><title>CyberLab Training Server</title></head>
<body><h1>Authorized Ethical Hacking Lab</h1>
<p>This synthetic target is intentionally misconfigured for coursework.</p>
<a href='/admin/'>Admin</a></body></html>"""
            self._headers(length=len(body))
            self.wfile.write(body)
        elif self.path == "/robots.txt":
            body = b"User-agent: *\nDisallow: /admin/\nDisallow: /backup/\n"
            self._headers(content_type="text/plain", length=len(body))
            self.wfile.write(body)
        elif self.path in ("/admin/", "/admin"):
            body = b"<html><body><h2>Directory listing for /admin/</h2><a href='notes.txt'>notes.txt</a></body></html>"
            self._headers(length=len(body))
            self.wfile.write(body)
        elif self.path == "/backup.zip":
            body = b"PK\x03\x04SYNTHETIC-TRAINING-BACKUP-NOT-A-REAL-ARCHIVE"
            self._headers(content_type="application/zip", length=len(body))
            self.wfile.write(body)
        else:
            body = b"Not Found"
            self._headers(status=404, content_type="text/plain", length=len(body))
            self.wfile.write(body)

    def do_HEAD(self):
        self._headers(length=0)

    def do_OPTIONS(self):
        body = b"GET, HEAD, OPTIONS, TRACE"
        self.send_response(200)
        self.send_header("Allow", "GET, HEAD, OPTIONS, TRACE")
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_TRACE(self):
        # Intentionally enabled only inside the isolated coursework target.
        raw = f"TRACE {self.path} {self.request_version}\r\n".encode()
        body = raw + b"Training-Only: true\r\n"
        self._headers(content_type="message/http", length=len(body))
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print("HTTP", self.address_string(), "-", fmt % args, flush=True)


def banner_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, BANNER_PORT))
        sock.listen(20)
        while True:
            conn, _addr = sock.accept()
            with conn:
                conn.sendall(b"SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.10\r\n")


if __name__ == "__main__":
    threading.Thread(target=banner_server, daemon=True).start()
    server = HTTPServer((HOST, HTTP_PORT), LabHandler)
    print(f"Controlled HTTP target listening on http://{HOST}:{HTTP_PORT}", flush=True)
    print(f"Synthetic banner service listening on {HOST}:{BANNER_PORT}", flush=True)
    server.serve_forever()
