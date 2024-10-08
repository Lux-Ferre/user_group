import json
from typing import Any


def json_encode(input_data: Any) -> str:
    output = ''
    if type(input_data) == str:
        output = f'"{input_data}"'
    if type(input_data) in [int, float, bool]:
        output = str(input_data).lower()
    if input_data is None:
        output += 'null'
    if type(input_data) in [list, tuple]:
        output += '[{}]'.format(', '.join(
            [json_encode(value) for _, value in enumerate(input_data)]))
    if type(input_data) == dict:
        output += '{{{}}}'.format(", ".join(
            [f'"{repr(key)}": {json_encode(value)}'
             for key, value in input_data.items()]))
    return output

def fix_dict(data: Any) -> Any:
    if type(data) == list:
        return [fix_dict(e) for e in data]
    if type(data) == dict:
        new_dict =  {}
        for k, v in data.items():
            if "'" in k:
                new_key = k.replace("'", "")
            elif "." in k or "e" in k:
                new_key = float(k)
            else:
                new_key = int(k)
            new_dict[new_key] = fix_dict(v)
        return new_dict
    return data

def json_decode(jsons: str) -> Any:
    return fix_dict(json.loads(jsons))

if __name__ == '__main__':
    object_to_translate = ['a', 1, 2, True, [5, 6], {
        'test': 1,
        'test2': [8, 9],
        3: {
            'a': 'b',
            'c': 'd'
        },
        77: [{'x': 0}, {'y': None}],
        1.5: "foo",
        "1.5": "bar",
        1e50: "big float"
    }]
    #object_to_translate = {1:"something","1":"something else"}
    result = json_encode(object_to_translate)
    print(result)
    dump = json.dumps(object_to_translate)
    print(result == dump)
    test = json_decode(result)
    print(test)
    print(test == object_to_translate)
