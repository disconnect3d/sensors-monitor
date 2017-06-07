import json
import socketserver
import socket

import arrow as arrow
from django.core.management.base import BaseCommand

from sensors.models import Sensor, MeasurementValue


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ThreadedMeasurementsPostHandler(socketserver.BaseRequestHandler):
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

    def _error(self, msg):
        self.request.send(self._raw_data({'status': 'error', 'message': msg}))

    def _success(self):
        self.request.send(self._raw_data({'status': 'success'}))

    @staticmethod
    def _raw_data(dict_data):
        return bytes(json.dumps(dict_data), 'utf8')

    def handle(self):
        data = self.get_json()

        self.stdout.write("Got data={}".format(data))

        if set(data.keys()) != {'host', 'host_key', 'sensors'}:
            self._error('Wrong fields. Required: host, sensors')
            return

        for sensor in data['sensors']:
            if sensor.keys() != {'kind', 'values'}:
                self._error('Wrong sensor fields. Required: kind, values')
                return

        host = data['host']

        for sensor in data['sensors']:
            try:
                s = Sensor.objects.get(host__name=host, host__host_key=data['host_key'], kind__kind_name=sensor['kind'])

            except Sensor.DoesNotExist:
                self._error('Sensor does not exist for given data or wrong host_key. Host={}, kind={}'.format(host, sensor['kind']))
                return

            def create_measurement(value, time):
                return MeasurementValue(
                    sensor=s,
                    value=value,
                    measurement_time=arrow.get(time).datetime,
                    upload_time=arrow.utcnow().datetime
                )

            MeasurementValue.objects.bulk_create(
                [create_measurement(value, time) for (time, value) in sensor['values']]
            )
        self._success()

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
        ThreadedMeasurementsPostHandler.stdout = self.stdout
        ThreadedMeasurementsPostHandler.stderr = self.stderr

        socket.setdefaulttimeout(90)

        with socketserver.TCPServer((host, port), ThreadedMeasurementsPostHandler) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            server.serve_forever()
