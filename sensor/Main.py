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
parser.add_option("-s", "--server", dest="server", default="localhost",
                  help="server ip", metavar="SERVER")
parser.add_option("-p", "--port", dest="port", default=9000,
                  help="tcp port of server", metavar="PORT")
(options, args) = parser.parse_args()


json_base = {
    'host': options.name,
}

measures = Measures.combined()
measurement_date = arrow.utcnow().timestamp

packet = Serializer.packets(json_base, measurement_date, measures)

Networking.open_connection(options.server, options.port)
print(packet)
Networking.send(packet)
Networking.close_connection()
