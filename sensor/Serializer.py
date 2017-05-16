import json


def packets(json_base, measurement_date, measures):
    json_objects = []
    json_strings = []
    for key, value in measures.items():
        new_json = json_base.copy()
        new_json["kind"] = key
        new_json["values"] = [[measurement_date, value]]
        json_objects.append(new_json)

    for json_data in json_objects:
        single_json = json.dumps(json_data)
        json_strings.append(single_json)

    return json_strings
