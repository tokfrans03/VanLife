#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from send import send
import requests
import ssl
import os
import subprocess
import datetime
port = 8000
config = {}
manifest = []
Allowed_actions = ["rf", "get", "notif",
                   "addnotif", "removenotif", "update", "command", "location"]
config_file = 'config.json'
location_file = 'platser.json'


def sendnotif(title, message):

    urls = []
    names = []
    errors = []

    for x in config["notif"]:
        names.append(x["name"])
        urls.append("https://pushalarm.de/pushout.php?grouptoken=" +
                    x["grouptoken"]+"&alert="+title+"&content="+message)

    for url, n in zip(urls, range(len(urls))):
        # res = json.loads(requests.get(url).text)
        # if res["status"] != 1:
        #     errors.append(names[n])
        res = requests.get(url).text
        if "Notification successfully sent" not in res:
            errors.append(names[n])

    names = ", ".join(names)
    errors = ", ".join(errors)
    if errors:
        return [False, "Skickat till " + names + ". Men misslyckades att skicka till " + errors + " (De kanske har bytt svar strukturen, fråga Martin)"]
    return [True, "Skickat till " + names]

    # if image == "":
    # else:
    #     url = "https://api.pushmealert.com?user="+user+"&key="+key+"&title="+title+"&message="+message+"&image=" + image


def refreshConfig():
    global config
    global manifest
    with open(config_file) as json_file:
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

        if body["action"] == "rf":  # checks for rf values
            if type(body["value"]) != int:
                return [False, "rf value must be an int"]

        if body["action"] == "notif":  # checks for notif
            if type(body["value"]) != dict:
                return [False, "Value must be a dict contaning a title and message"]
            if "title" not in body["value"]:
                return [False, "Value must contain a title"]
            if "message" not in body["value"]:
                return [False, "Value must contain a message"]

        if body["action"] == "addnotif":  # checks for addnotif
            if type(body["value"]) != dict:
                return [False, "Value must be a dict contaning a title and message"]
            # if "user" not in body["value"]:
            #     return [False, "Value must contain a user"]
            if "group" not in body["value"]:
                return [False, "Value must contain a group"]
            if "name" not in body["value"]:
                return [False, "Value must contain a name"]

        if body["action"] == "removenotif":  # checks for removenotif
            if type(body["value"]) != dict:
                return [False, "Value must be a dict contaning a name"]
            if "name" not in body["value"]:
                return [False, "Value must contain a name"]

        if body["action"] == "update":  # checks for update
            if type(body["value"]) != str:
                return [False, "Value must be a string"]

        if body["action"] == "command":  # checks for removenotif
            if type(body["value"]) != str:
                return [False, "Value must be a string"]

        if body["action"] == "location":  # checks for removenotif
            if type(body["value"]) != str:
                return [False, "Value must be a string"]

        return [True]
    except:
        return [False, "unknown error"]


class S(BaseHTTPRequestHandler):
    def send_res(self, args, code=200, Success=True):

        self.send_response(code)
        self.send_header('Content-type', 'application/json')
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

        print("\nGET Path:", self.path)
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
        print("\nPOST Path:", str(self.path),
              "\nHeaders:\n" + str(self.headers))
        print(content_length)
        if content_length > 0:
            body = post_data.decode('utf-8')
            print("Body:\n" + body, "\n")
            if checkbody(body)[0] == True:  # all good
                body = json.loads(body)
                if body["action"] == "rf":
                    send(body["value"])
                    self.send_res("Done!")
                # TODO
                elif body["action"] == "notif":
                    try:
                        body = body["value"]

                        res = sendnotif(body["title"], body["message"])
                        if res[0]:
                            self.send_res(res[1])  # success
                        else:  # error
                            self.send_res(res[1], Success=False, code=201)
                        return
                    except IndexError:
                        self.send_res(
                            "Index out of range, try sending a message", code=500, Success=False)
                        return
                    except Exception as e:
                        print(e)
                        self.send_res("Something went wrong: " +
                                      e, code=500, Success=False)
                        return
                elif body["action"] == "addnotif":
                    try:
                        body = body["value"]
                        config["notif"].append(body)
                        with open("config.json", "w+", encoding='utf-8') as json_file:
                            json.dump(config, json_file)
                        refreshConfig()
                        self.send_res("Lade till " + body["name"])
                        return
                    except Exception as e:
                        print(e)
                        self.send_res("Something went wrong: " +
                                      e, code=500, Success=False)
                        return
                elif body["action"] == "removenotif":
                    try:
                        body = body["value"]
                        removed = False
                        for x, n in zip(config["notif"], range(len(config["notif"]))):
                            if x["name"] == body["name"]:
                                config["notif"].pop(n)
                                removed = True
                        with open(config_file, "w+", encoding='utf-8') as json_file:
                            json.dump(config, json_file)
                        refreshConfig()
                        if removed:
                            self.send_res("Tog bort till " + body["name"])
                        else:
                            self.send_res("Hittade inte '" +
                                          body["name"] + "'", Success=False)
                        return
                    except Exception as e:
                        print(e)
                        self.send_res("Something went wrong: " +
                                      e, code=500, Success=False)
                        return

                elif body["action"] == "update":
                    try:
                        url = body["value"]
                        self.send_res("Klar! laddar om...")
                        os.system("sh update.sh " + url)
                        return
                    except Exception as e:
                        print(e)
                        self.send_res("Something went wrong: " +
                                      e, code=500, Success=False)
                        return

                elif body["action"] == "command":
                    self.send_res(subprocess.run(body["value"].split(" "), stdout=subprocess.PIPE).stdout.decode(
                        'utf-8').replace("\n", "<br/>").replace(" ", "&nbsp;"))
                    return

                elif body["action"] == "location":
                    datum = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                    with open(location_file) as loc_file:
                        loc = json.load(loc_file)

                    loc["locations"].append({"location": body["value"], "date": datum})

                    with open(location_file, "w+", encoding='utf-8') as loc_file:
                        json.dump(loc, loc_file)

                    self.send_res("Plats sparad")
                    return


            else:  # Body is wrong

                print(checkbody(body)[1])
                self.send_res(checkbody(body)[1], Success=False)

        else:
            self.send_res(
                "POST request for {} . Please send a body".format(self.path), Success=False)


def run(server_class=HTTPServer, handler_class=S, port=port):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.socket = ssl.wrap_socket(
        httpd.socket, certfile='/root/.https-serve/server.pem', server_side=True)

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
