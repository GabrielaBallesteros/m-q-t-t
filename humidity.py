#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 10:22:28 2023


4 Temperatura y humedad
Elige un termómetro concreto al que escuchar,es decir, uno de los sensores que 
publican en temperature. Escribe ahora el código para un cliente mqtt cuya 
misión es escuchar un termómetro y, si su valor supera una determinada temperatura,
K 0, entonces pase a escuchar también en el topic humidity. Si la temperatura 
baja de K 0 o el valor de humidity sube de
K 1 entonces el cliente dejará de escuchar en el topic humidity.
"""

from paho.mqtt.client import Client
import sys

K0 = 30
K1 = 100

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)
    n = float (msg.payload)
    if msg.topic == 'humidity':
        if n > K1:
            client.unsubscribe('humidity')
            userdata['humidity'] = "no suscrito"
    elif msg.topic == 'temperature/t2':
        if n > K0 and userdata['humidity'] == "no suscrito":
            client.subscribe('humidity')
            userdata['humidity'] = "suscrito" 
        elif n < K0 and userdata['humidity'] == "suscrito":
            client.unsubscribe('humidity') 
            userdata['humidity'] = "no suscrito"
    elif msg.topic == 'humidity':
        if n > K1:
            client.unsubscribe('humidity')
            userdata['humidity'] = "no suscrito"
            
def main(hostname):
    userdata = {
        'humidity':"no suscrito"
    }
    client = Client(userdata= userdata)
    client.on_message = on_message

    print(f'Connecting on channels numbers on {hostname}')
    client.connect(hostname)

    client.subscribe('temperature/t2')

    client.loop_forever()

if __name__ == "__main__":
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
    broker = sys.argv[1]
    main(broker)
