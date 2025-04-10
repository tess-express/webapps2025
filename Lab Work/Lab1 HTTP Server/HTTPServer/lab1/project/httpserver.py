from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime


class HttpServer(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == '/webapps':
            self.send_response(200)
            self.send_header("content-type", "text/html;charset=utf-8")
            self.send_header("user-agent", "aa")
            self.end_headers()
            self.wfile.write(bytes(str(datetime.now()), "utf-8"))
            
        else:
            m = "Unsupported URI: " + self.path
            self.send_error(400, m)
       


httpd = HTTPServer(('localhost', 10000), HttpServer)
httpd.serve_forever()
