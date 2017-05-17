from optparse import OptionParser
import arrow

import measures
import serializer
import networking

# Parse arguments
parser = OptionParser()
parser.add_option("-n", "--name", dest="name", default="NeckBook-Pro",
                  help="name this pc", metavar="NAME")
parser.add_option("-s", "--server", dest="server", default="disconnect3d.pl",
                  help="server ip", metavar="SERVER")
parser.add_option("-p", "--port", dest="port", default=31337,
                  help="tcp port of server", metavar="PORT")
(options, args) = parser.parse_args()


json_base = {
    'host': options.name,
}

networking.open_connection(options.server, options.port)

while 1:
    try:
        retrieved_measures = measures.combined()
        measurement_date = arrow.utcnow().timestamp

        packet = serializer.packets(json_base, measurement_date, retrieved_measures)

        print(packet)
        networking.send(packet)
    except KeyboardInterrupt:
        break


networking.close_connection()
