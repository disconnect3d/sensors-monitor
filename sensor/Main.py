from optparse import OptionParser
# from datetime import datetime
import uuid

import Measures
import Serializer
import Networking
import arrow

# Parse arguments
parser = OptionParser()
parser.add_option("-n", "--name", dest="name", default=str(uuid.uuid1().urn[4:]),
                  help="name this pc", metavar="NAME")
parser.add_option("-s", "--server", dest="server", default="disconnect3d.pl",
                  help="server ip", metavar="SERVER")
parser.add_option("-p", "--port", dest="port", default=31337,
                  help="tcp port of server", metavar="PORT")
(options, args) = parser.parse_args()


json_base = {
    'host': options.name,
}

Networking.open_connection(options.server, options.port)

while 1:
    try:
        measures = Measures.combined()
        measurement_date = arrow.utcnow().timestamp

        packet = Serializer.packets(json_base, measurement_date, measures)

        print(packet)
        Networking.send(packet)
    except KeyboardInterrupt:
        break


Networking.close_connection()
