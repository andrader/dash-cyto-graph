import json

def dump_json(obj, path):
    with open(path, 'w') as f:
        json.dump(obj, f)

def load_json(path):
    with open(path, 'r') as f:
        obj = json.load(f)
    return obj
