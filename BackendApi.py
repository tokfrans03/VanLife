#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from send import send
port = 8000
config = {}
manifest = []
Allowed_actions = ["rf", "get"]


def refreshConfig():
    global config
    global manifest
    with open('config.json') as json_file:
        config = json.load(json_file)
        manifest = []
        for x in config:
            manifest.append("/" + x)


refreshConfig()


def checkbody(body):
    try:
        try:
            body = json.loads(body)
        except:
            return [False, "Unable to parse json"]

        if "action" not in body:
            return [False, "No 'action' in body"]

        if "value" not in body:
            return [False, "No 'value' in body"]

        if type(body["action"]) != str:
            return [False, "'action' value must be a string"]

        if body["action"] not in Allowed_actions:
            return [False, "Action '" + body["action"] + "' not allowed"]

        if body["action"] == "rf":
            if type(body["value"]) != int:
                return [False, "rf value must be an int"]

        return [True]
    except:
        return [False, "unknown error"]


class S(BaseHTTPRequestHandler):
    def send_res(self, args, code=200, Success=True):
        
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        out = {
            "Success": Success,
            "value": args
        }
        self.wfile.write(json.dumps(out).encode('utf-8'))

    def do_OPTIONS(self):
        print("\nPath:", str(self.path),
              "\nHeaders:\n" + str(self.headers))
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_GET(self):

        print("\nPath:", self.path)
        print(self.headers)

        if self.path == "/":
            self.send_res({"config": config})
            return

        # if self.path == "/":
        #     self.send_res({"Allowed-Methods": manifest})
        #     return

        if self.path in manifest:
            databack = config[self.path[1:]]
            self.send_res({"Allowed-Methods": databack})
            return

        if self.path == "/refresh":
            refreshConfig()
            self.send_res("")
            return

        self.send_res("No such method", code=404)

        # if self.path == "/mqtt":
        #     self._set_response(data)
        # else:
        #     self._set_response()

        # print("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        # self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        # <--- Gets the size of data
        content_length = int(self.headers['Content-Length'])
        # <--- Gets the data itself
        post_data = self.rfile.read(content_length)
        # print(json.loads(post_data.decode('utf-8')))
        print("\nPath:", str(self.path),
              "\nHeaders:\n" + str(self.headers))
        print(content_length)
        if content_length > 0:
            body = post_data.decode('utf-8')
            print("Body:\n" + post_data.decode('utf-8'), "\n")
            if checkbody(body)[0] == True:  # all good

                body = json.loads(body)
                if body["action"] == "rf":
                    send(body["value"])
                # TODO

                self.send_res("Done")

            else:  # Body is wrong

                print(checkbody(body)[1])
                self.send_res(checkbody(body)[1], Success=False)

        else:
            self.send_res(
                "POST request for {} . Please send a body".format(self.path), Success=False)


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
