#!/usr/bin/env python3
"""
Temporary HTTPS server that serves the publish JS and screenshot files.
Uses a self-signed cert so Chrome on HTTPS pages can fetch from it.

Usage:
    python3 upload_server.py

Then in Chrome console on thrivethemes.com/wp-admin, run:
    fetch('https://localhost:9443/publish_screenshots.js').then(r=>r.text()).then(eval)

You'll need to first visit https://localhost:9443 in Chrome and accept the cert.
"""
import http.server
import json
import os
import ssl
import subprocess
import sys

PORT = 9443
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Generate self-signed cert
CERT_FILE = "/tmp/screenshot_server.pem"
if not os.path.exists(CERT_FILE):
    subprocess.run([
        "openssl", "req", "-new", "-x509",
        "-keyout", CERT_FILE, "-out", CERT_FILE,
        "-days", "1", "-nodes",
        "-subj", "/CN=localhost"
    ], capture_output=True)
    print(f"Generated self-signed cert: {CERT_FILE}")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(CERT_FILE)

    with http.server.HTTPServer(("", PORT), Handler) as httpd:
        httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
        print(f"\n{'='*60}")
        print(f"HTTPS server running on https://localhost:{PORT}")
        print(f"Serving files from: {BASE_DIR}")
        print(f"\nStep 1: Visit https://localhost:{PORT} in Chrome")
        print(f"        and accept the security warning")
        print(f"\nStep 2: In Chrome console on thrivethemes.com/wp-admin:")
        print(f"        fetch('https://localhost:{PORT}/publish_screenshots.js')")
        print(f"          .then(r=>r.text()).then(eval)")
        print(f"{'='*60}\n")
        httpd.serve_forever()
