import json
import arrow


def packets(json_base, measurement_date, measures):
    json_objects = []
    json_string = json_base.copy()
    registration_date = arrow.get("2017-05-16 00:00:00", 'YYYY-MM-DD HH:mm:ss').timestamp

    for key, value in measures.items():
        new_json = {}
        new_json["kind"] = key
        new_json["values"] = [[measurement_date, value]]
        new_json["registered_at"] = registration_date
        json_objects.append(new_json)

    json_string["sensors"] = json_objects

    return json.dumps(json_string)
