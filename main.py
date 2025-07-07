import http.server
import socketserver
import urllib.parse
import os
from datetime import datetime

PORT = 8080

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/submit-message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            fields = urllib.parse.parse_qs(post_data)

            name = fields.get('name', [''])[0]
            email = fields.get('email', [''])[0]
            message = fields.get('message', [''])[0]
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save to file
            with open("messages.txt", "a") as f:
                f.write(f"\n---\nTime: {time_now}\nName: {name}\nEmail: {email}\nMessage: {message}\n")

            self.send_response(303)
            self.send_header('Location', '/thankyou.html')
            self.end_headers()
        else:
            self.send_error(404)

# Start the server
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()

