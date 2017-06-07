#!/usr/bin/env python
from argparse import ArgumentParser
import arrow

import measures
import serializer
import networking

# Parse arguments
parser = ArgumentParser()
parser.add_argument('name', help='name this pc', metavar='NAME')
parser.add_argument('host', help='server ip', metavar='SERVER')
parser.add_argument('port', help='tcp port of server', metavar='PORT')
parser.add_argument('host_key', help='host key', metavar='HOSTKEY')
args = parser.parse_args()


json_base = {
    'host': args.name,
    'host_key': args.host_key
}


def send_data(packet):
    networking.open_connection(args.host, int(args.port))
    networking.send(packet)
    response = networking.recv()
    networking.close_connection()

    if response['status'] != 'success':
        raise Exception(response['message'])

    return True


while 1:
    try:
        retrieved_measures = measures.combined()
        measurement_date = arrow.utcnow().timestamp

        packet = serializer.packets(json_base, measurement_date, retrieved_measures)
        print(packet)

        while not send_data(packet):
            pass

    except KeyboardInterrupt:
        break


print("closing connection")
networking.close_connection()
