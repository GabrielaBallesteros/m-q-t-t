#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 10:18:45 2023

2 Números
En el topic numbers se están publicando constantemente númeroslo, s hay enteros 
y los hay reales. Escribe el código de un cliente mqtt que lea este topic y que 
realice tareas con los números leídos,por ejemplo, separar los enteros y reales,
calcular la frecuencia de cada uno de ellos, estudiar propiedades (como ser o no 
primo) en los enteros, etc.
"""
from paho.mqtt.client import Client
import sys
from sympy import isprime

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)
    try:
        n = float(msg.payload)
        if n // 1 == 0.0:
            client.publish('/clients/reales',msg.payload)
            userdata['frecuencia']['reales'] += 1
            client.publish('/clients/frecreales', f'{userdata["frecuencia"]["reales"]}')
        else:
            n = int(msg.payload)
            primo = isprime(int(n))
            client.publish('/clients/enteros',f'{msg.payload} es primo: {primo}')
            userdata['frecuencia']['enteros'] += 1
            client.publish('/clients/frecenteros', f'{userdata["frecuencia"]["enteros"]}')
            userdata['suma']['suma'] += n
            client.publish('/clients/suma', f'{userdata["suma"]["suma"]}')
            if n % 2 == 0:
                client.publish('/clients/par', msg.payload)
            else:
                client.publish('/clients/impar', msg.payload)
            
        
    except ValueError:
        pass
    except Exception as e:
        raise e


def main(broker):
    userdata = {'suma' : {'suma':0},
                'frecuencia' :{'enteros':0,'reales':0}}
    client = Client(userdata=userdata)
    client.on_message = on_message

    print(f'Connecting on channels numbers on {broker}')
    client.connect(broker)

    client.subscribe('numbers')

    client.loop_forever()


if __name__ == "__main__":
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
    broker = sys.argv[1]
    main(broker)

