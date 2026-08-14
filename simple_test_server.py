import http.server
import socketserver

PORT = 9999

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Simple HTTP server running at http://0.0.0.0:{PORT}")
    print(f"Try accessing: http://localhost:{PORT}")
    print(f"Try accessing: http://192.168.0.102:{PORT}")
    print("Press Ctrl+C to stop")
    httpd.serve_forever()
