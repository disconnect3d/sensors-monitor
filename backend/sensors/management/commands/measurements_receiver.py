import json
import socketserver

import arrow as arrow
from django.core.management.base import BaseCommand

from sensors.models import Sensor, MeasurementValue


class MeasurementsPostHandler(socketserver.BaseRequestHandler):
    """
    Measurements TCP Server requests handler.
    
    Expects JSON:
     {
        'host': <host name>,
        'kind': <sensor kind name>,
        'registered_at': <datetime?>,
        'values': [[time1, val1], [time2, val2], ...]
     }
     
     Where timeX is some time data (datetimes or seconds after epoch) and valX is value in that particular time.
    """

    def handle(self):
        data = self.get_json()

        self.stdout.write("Got data={}".format(data))

        if set(data.keys()) != {'host', 'kind', 'registered_at', 'values'}:
            self.request.send('Wrong fields. Required: host, kind, registered_at, values')
            return

        s = Sensor.objects.get(host__name=data['host'], kind__name=data['kind'], registered_at=data['registered_at'])

        def create_measurement(value, time):
            return MeasurementValue(
                sensor=s,
                value=value,
                measurement_time=time,
                upload_time=arrow.utcnow()
            )

        MeasurementValue.objects.bulk_create(
            [create_measurement(value, time) for (value, time) in data['values']]
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
        parser.add_argument('--host', nargs='?', type=str, default='0.0.0.0', required=False)
        parser.add_argument('-p', '--port', nargs='?', type=int, default=9000, required=False)

    def handle(self, *args, **options):
        host, port = options['host'], options['port']

        self.stdout.write(self.style.SUCCESS('Hosting measurements TCP server at %s:%d' % (host, port)))

        # fixme/hacky way to get stdout writer in request handler...
        MeasurementsPostHandler.stdout = self.stdout

        with socketserver.TCPServer((host, port), MeasurementsPostHandler) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            server.serve_forever()
