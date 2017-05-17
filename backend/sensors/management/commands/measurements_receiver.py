import json
import socketserver
import socket

import arrow as arrow
from django.core.management.base import BaseCommand

from sensors.models import Sensor, MeasurementValue


socket.setdefaulttimeout(90)


class MeasurementsPostHandler(socketserver.BaseRequestHandler):
    """
    Measurements TCP Server requests handler.

    Expects JSON:
     {
        "host": <host name>,
        "sensors": [ 
            {
                "kind": <sensor kind name>,
                "registered_at": <datetime?>,
                "values": [[time1, val1], [time2, val2], ...]
            },
            ...
        ]
     }

     Where timeX is some time data (datetimes or seconds after epoch) and valX is value in that particular time.
    """

    def handle(self):
        # receive as much measurements as possible
        # if client fails, we will just timeout
        while True:
            data = self.get_json()

            self.stdout.write("Got data={}".format(data))

            if set(data.keys()) != {'host', 'sensors'}:
                self.request.send('Wrong fields. Required: host, sensors')
                return

            for sensor in data['sensors']:
                if sensor.keys() != {'kind', 'registered_at', 'values'}:
                    self.request.send('Wrong sensor fields. Required: kind, registered_at, values')
                    return

            host = data['host']

            for sensor in data['sensors']:
                sensor['registered_at'] = arrow.get(sensor['registered_at']).datetime

                try:
                    s = Sensor.objects.get(host__name=host, kind__kind_name=sensor['kind'], registered_at=sensor['registered_at'])
                except Sensor.DoesNotExist:
                    self.stderr.write('Sensor does not exist. Host={}, kind={}, registered_at={}'.format(host, sensor['kind'], sensor['registered_at']))
                    continue

                def create_measurement(value, time):
                    #print(value, time)
                    return MeasurementValue(
                        sensor=s,
                        value=value,
                        measurement_time=arrow.get(time).datetime,
                        upload_time=arrow.utcnow().datetime
                    )

                MeasurementValue.objects.bulk_create(
                    [create_measurement(value, time) for (time, value) in sensor['values']]
                )

    def get_json(self):
        buf = self.request.recv(1024)

        while True:
            try:
                return json.loads(buf)

            except ValueError:
                # if json can't be decoded, we didn't receive all of it
                buf += self.request.recv(1024)


class Command(BaseCommand):
    help = 'Serves TCP server for sensors measurements'

    def add_arguments(self, parser):
        parser.add_argument('--host', nargs='?', type=str, default='localhost', required=False)
        parser.add_argument('-p', '--port', nargs='?', type=int, default=9000, required=False)

    def handle(self, *args, **options):
        host, port = options['host'], options['port']

        self.stdout.write(self.style.SUCCESS('Hosting measurements TCP server at %s:%d' % (host, port)))

        # fixme/hacky way to get stdout/stderr writer in request handler...
        MeasurementsPostHandler.stdout = self.stdout
        MeasurementsPostHandler.stderr = self.stderr


        with socketserver.TCPServer((host, port), MeasurementsPostHandler) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            server.serve_forever()
