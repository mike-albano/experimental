import http.server
import socketserver

port = 80
handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", port), handler)
print("serving at port:" + str(port))
httpd.serve_forever()
