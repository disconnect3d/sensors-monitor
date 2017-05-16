from optparse import OptionParser
from datetime import datetime
import uuid

import Measures
import Serializer


# Parse arguments
parser = OptionParser()
parser.add_option("-n", "--name", dest="name", default=str(uuid.uuid1().urn[4:]),
                  help="name this pc", metavar="NAME")
(options, args) = parser.parse_args()


json_base = {
    'host': options.name,
    'registered_at': 's'
}

measures = Measures.combined()
measurement_date = str((datetime.now() - datetime.fromtimestamp(0)).total_seconds())

packets = Serializer.packets(json_base, measurement_date, measures)

for jsonString in packets:
    print(jsonString)

