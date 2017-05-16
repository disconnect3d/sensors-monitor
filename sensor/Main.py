import os
import psutil
from optparse import OptionParser
from datetime import datetime
import json
import uuid


# Parse arguments
parser = OptionParser()
parser.add_option("-n", "--name", dest="name", default=str(uuid.uuid1().urn),
                  help="name this pc", metavar="NAME")
(options, args) = parser.parse_args()


memoryUse = psutil.virtual_memory()
totalMemory = memoryUse.total
availableMemory = memoryUse.available
usedPercentMemory = memoryUse.percent
memory = {
    'total': memoryUse.total,
    'available': memoryUse.available,
    'usedPercent': memoryUse.percent
}
print(memory)

cpuPercent = psutil.cpu_percent(percpu=True)
# cpuPercent = psutil.cpu_percent(interval=1, percpu=True)
cores = {}
counter = 0
for cpu in cpuPercent:
    cores['Core '+str(counter)] = cpu
    counter += 1
print(cores)

jsonData = {
    'name': options.name,
    'memory': memory,
    'cpu': cores
}

json = json.dumps(jsonData)
print(json)


# psutil.sensors_temperatures()
# psutil.sensors_fans()
# psutil.sensors_battery()


# print('memory use:', memoryUse)
# print('cpu use:', cpuPercent)