import json
from pydantic import BaseModel
from base64 import b64encode, b64decode


def __fill_class(model_json, model_class):
    fields = model_class.__fields__
    new_json = {}
    for key in model_json:
        print(key, fields[key].type_)
        if key in fields and issubclass(fields[key].type_, BaseModel) and model_json[key] is not None:
            new_json[key] = __fill_class(model_json[key], fields[key].type_)
        elif key in fields:
            new_json[key] = model_json[key]

    return model_class(**new_json)
        


def serialize(model):
    s = str(b64encode(model.json().encode()))
    return s[2:-1]



def deserialize(s, model_class=None):
    s = f"b'{s}'"
    model_json = json.loads(b64decode(eval(s)))
    if model_class:
        return __fill_class(model_json, model_class)
    return model_json