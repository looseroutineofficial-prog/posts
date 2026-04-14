import http.server, os, sys

PORT = 8769
DIR  = os.path.dirname(os.path.abspath(__file__))

os.chdir(DIR)
print(f"Serving {DIR} at http://localhost:{PORT}")

handler = http.server.SimpleHTTPRequestHandler
httpd = http.server.HTTPServer(("", PORT), handler)
httpd.serve_forever()
