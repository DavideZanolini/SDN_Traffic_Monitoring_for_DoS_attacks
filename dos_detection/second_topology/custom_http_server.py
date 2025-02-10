from http.server import HTTPServer, BaseHTTPRequestHandler

class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"GET request received")

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length else b''
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"POST request received. Data: " + post_data)

    def do_PATCH(self):
        content_length = int(self.headers.get('Content-Length', 0))
        patch_data = self.rfile.read(content_length) if content_length else b''
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"PATCH request received. Data: " + patch_data)

    def do_PUT(self):
        content_length = int(self.headers.get('Content-Length', 0))
        put_data = self.rfile.read(content_length) if content_length else b''
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"PUT request received. Data: " + put_data)

    def do_DELETE(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"DELETE request received")
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Allow", "GET, POST, PATCH, PUT, DELETE, OPTIONS")
        self.end_headers()

if __name__ == "__main__":
    server_address = ('', 80)  # Listen on port 80
    httpd = HTTPServer(server_address, CustomHandler)
    print("Serving on port 80...")
    httpd.serve_forever()
