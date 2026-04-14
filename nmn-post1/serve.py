import http.server, os
PORT = 8770
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"http://localhost:{PORT}/nmn_post1.html")
http.server.HTTPServer(("", PORT), http.server.SimpleHTTPRequestHandler).serve_forever()
