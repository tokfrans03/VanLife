#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
port = 8000
config = {}
manifest = []

def refreshConfig():
    global config
    global manifest
    with open('config.json') as json_file:
        config = json.load(json_file)
        manifest = []
        for x in config:
            manifest.append("/" + x)

refreshConfig()

class S(BaseHTTPRequestHandler):
    def send_res(self, args, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(args).encode('utf-8'))

    def do_GET(self):

        print("Path:", self.path)
        print(self.headers)

        if self.path == "/":
            self.send_res({"Allowed-Methods": manifest})
            return

        if self.path in manifest:
            databack = config[self.path[1:]]
            self.send_res({"Allowed-Methods": databack})
            return

        if self.path == "/refresh":
            refreshConfig()

        self.send_res("No such method", code=404)


        # if self.path == "/mqtt":
        #     self._set_response(data)
        # else:
        #     self._set_response()


        # print("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        # self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self.send_res()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=port):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port', port, '...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('\nStopping httpd...')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()