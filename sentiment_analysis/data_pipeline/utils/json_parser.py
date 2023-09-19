import json


def recursively_parse_json(data):
    if isinstance(data, str):
        try:
            return recursively_parse_json(json.loads(data))
        except ValueError:
            return data
    elif isinstance(data, list):
        return [recursively_parse_json(item) for item in data]
    elif isinstance(data, dict):
        return {key: recursively_parse_json(value) for key, value in data.items()}
    else:
        return data
