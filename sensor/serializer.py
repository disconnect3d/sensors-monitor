import json


def packets(json_base, measurement_date, retrieved_measures):
    sensors = []
    json_string = json_base.copy()

    for key, value in retrieved_measures.items():
        sensors.append({
            'kind': key,
            'values': [[measurement_date, value]]
        })
    json_string["sensors"] = sensors

    return json.dumps(json_string)
