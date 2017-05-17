import json
import arrow


def packets(json_base, measurement_date, measures):
    sensors = []
    json_string = json_base.copy()
    registration_date = arrow.get("2017-05-16 00:00:00", 'YYYY-MM-DD HH:mm:ss').timestamp

    for key, value in measures.items():
        sensors.append({
            'kind': key,
            'values': [[measurement_date, value]],
            'registered_at': registration_date
        })
    json_string["sensors"] = sensors

    return json.dumps(json_string)
