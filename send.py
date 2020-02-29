#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rpi_rf import RFDevice

GPIO = 17
repeat = 10

rfdevice = RFDevice(GPIO)
rfdevice.enable_tx()
rfdevice.tx_repeat = repeat

protocol = 1
pulselength = 390
length = 24

def send(code):
    rfdevice.tx_code(code, protocol, pulselength, length)


if __name__ == "__main__":

    codes = [
        {
            "name": "Av/På",
            "code": 4353281
        },
        {
            "name": "Light",
            "code": 4353284
        },
        {
            "name": "Bright +",
            "code": 4353285
        },
        {
            "name": "Bright -",
            "code": 4353286
        },
        {
            "name": "100%",
            "code": 4353287
        },
        {
            "name": "50%",
            "code": 4353288
        },
        {
            "name": "25%",
            "code": 4353289
        },
        {
            "name": "Mode +",
            "code": 4353291
        },
        {
            "name": "Mode -",
            "code": 4353297
        },
        {
            "name": "Speed +",
            "code": 4353295
        },
        {
            "name": "Speed -",
            "code": 4353293
        }
    ]

    while 1:
        y = 0

        for x in codes:
            y += 1
            print(y, ":", x["name"])

        try:
            val = int(input("\nVal:\n> "))
            if val > len(codes):
                raise ValueError
        except ValueError:
            print("inte ett nummer / tillåtet tal, stänger Av/På")
            val = 1
        except KeyboardInterrupt:
            print("\nAvslutar...")
            exit()

        print("Skickar:", codes[val - 1]["code"], "\n")

        rfdevice.tx_code(codes[val - 1]["code"], protocol, pulselength, length)
