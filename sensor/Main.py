import os
import psutil
from optparse import OptionParser
from datetime import datetime
import json
import uuid


# Parse arguments
parser = OptionParser()
parser.add_option("-n", "--name", dest="name", default=str(uuid.uuid1().urn[4:]),
                  help="name this pc", metavar="NAME")
(options, args) = parser.parse_args()


memoryUse = psutil.virtual_memory()
totalMemory = memoryUse.total/1024/1024
availableMemory = memoryUse.available/1024/1024
usedPercentMemory = memoryUse.percent
memory = {
    'Total memory [MB]': memoryUse.total,
    'Available memory [MB]': memoryUse.available,
    'Used memory [%]': memoryUse.percent
}
print(memory)

cpuPercent = psutil.cpu_percent(percpu=True)
# cpuPercent = psutil.cpu_percent(interval=1, percpu=True)
cores = {}
counter = 0
for cpu in cpuPercent:
    cores['Core '+str(counter)+' [%]'] = cpu
    counter += 1
print(cores)

jsonBase = {
    'host': options.name,
    'registered_at': 's'
}

measurementDate = str(datetime.utcnow())

jsons = []
for key, value in memory.items():
    newJson = jsonBase.copy()
    newJson["kind"] = key
    newJson["values"] = [[measurementDate, value]]
    jsons.append(newJson)

for key, value in cores.items():
    newJson = jsonBase.copy()
    newJson["kind"] = key
    newJson["values"] = [[measurementDate, value]]
    jsons.append(newJson)

for jsonData in jsons:
    jsonString = json.dumps(jsonData)
    print(jsonString)

# json = json.dumps(jsonData)
# print(json)


# psutil.sensors_temperatures()
# psutil.sensors_fans()
# psutil.sensors_battery()


# print('memory use:', memoryUse)
# print('cpu use:', cpuPercent)