def create_deep_dict(value, layers):
    orig_data = {}
    data = orig_data
    last_layer = layers[-1]

    for layer in layers[:-1]:
        data[layer] = {}
        data = data[layer]

    data[last_layer] = value

    return orig_data


def fill_arr(data):
    arr_from_dict = []
    for i, key in enumerate(data):
        if len(data[key]) > 1:
            for j, inner_arr in enumerate(data[key]):
                arr_from_dict.append({key: inner_arr})
        else:
            arr_from_dict.append({key: data[key][0]})

    return arr_from_dict


def transform_list_to_dict(data):
    items = [{}] * len(data)
    for i, item in enumerate(data):
        for key in item:
            items[i] = create_deep_dict(key, item[key])
    return items


def merge(a, b, path=None):
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


if __name__ == '__main__':
    import json

    from json_parser import parse

    parsed = {}
    with open('translates/ru.json', 'r') as fp:
        parsed = json.load(fp)
    keys_by_translate = {}

    parse(parsed, [], 0, keys_by_translate)
    arr = fill_arr(keys_by_translate)
    arr = transform_list_to_dict(arr)

    cor_obj = arr[0]
    for obj in arr[1:]:
        cor_obj = merge(cor_obj, obj)

    with open('result.json', 'w') as fp:
        json.dump(cor_obj, fp, ensure_ascii=False, indent=4)
