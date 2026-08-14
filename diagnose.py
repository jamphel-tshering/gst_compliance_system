import http.server
import socketserver

print("Testing HTTP server on port 7777...")

PORT = 7777
Handler = http.server.SimpleHTTPRequestHandler

try:
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Simple HTTP server running on http://0.0.0.0:{PORT}")
        print(f"Try accessing: http://localhost:{PORT}")
        print(f"Try accessing: http://192.168.0.102:{PORT}")
        print(f"Press Ctrl+C to stop")
        httpd.serve_forever()
except Exception as e:
    print(f"Error starting server: {e}")
