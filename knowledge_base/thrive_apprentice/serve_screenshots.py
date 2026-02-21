#!/usr/bin/env python3
"""Simple HTTP server with CORS headers to serve screenshot files to Chrome."""
import http.server
import os

PORT = 8765
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")

class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    with http.server.HTTPServer(("", PORT), CORSHandler) as httpd:
        print(f"Serving screenshots from {DIR} on http://localhost:{PORT}")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()
