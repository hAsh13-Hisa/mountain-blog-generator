#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 8888
DIRECTORY = "static_site"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"サーバーを起動しました: http://localhost:{PORT}")
    print("停止するには Ctrl+C を押してください")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nサーバーを停止しました")