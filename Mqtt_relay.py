#!/usr/bin/env python3

import requests
import json
import paho.mqtt.client as mqtt

back_url = "http://192.168.0.97/"
url = "maqiatto.com"
port = 1883
id = 1

config = json.loads(requests.get(back_url).text)["value"]["config"]
# print(type(config) , config)


def send_res(args, Success=True):
    global id
    id += 1
    args["id"] = id
    out = json.dumps(args)
    print("Sending", out)

    client.publish(config["mqtt"]["topics"][0], out)

# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(config["mqtt"]["topics"][0])

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    print(msg.topic, str(msg.payload.decode("utf-8")))

    try:
        req = json.loads(str(msg.payload.decode("utf-8")))
        # print("good json")
    except:  # not json
        print("not json")
        send_res("not json", Success=False)
        return

    if "id" in req:  # no dupes
        # print("no dupes pls")
        return

    res = json.loads(requests.post(back_url, json.dumps(req)).text)


    send_res(res)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(config["mqtt"]["user"], password=config["mqtt"]["pass"])

client.connect(url, port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
try:
    client.loop_forever()
except:
    print("\nExit...")
    exit()
