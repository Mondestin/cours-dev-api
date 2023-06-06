import http.server as server #Parametrage: location, handler
import socketserver as socket #Ecoute

#Handler
class APIHandler(server.SimpleHTTPRequestHandler):
 def do_GET(self) -> None:
  print('hello')
  self.send_response(200)
  self.send_header('Content-Type','application/json')
  self.end_headers()
  self.wfile.write("coucou".encode('utf-8'))

#init apihandler
MyHandler = APIHandler

#server
try:
 with socket.TCPServer(("",8081), MyHandler) as httpd:
    print("sever started at port 8081")
    httpd.serve_forever()
except KeyboardInterrupt:
  print("Stopping server")
  httpd.server_close()
