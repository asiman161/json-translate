"""
Сравнивает 2 JSON'а и говориит о тех ключах, которые отсутствуют.
Корректная работа не гарантируется т.к. не проводилось точное тестирование
и что-то может быть пропущено

P.S. как оно работает - хз, чистая магия
"""
import json

ru = None
pt = None
global_keys = [None]

with open('translates/ru.json', 'r') as fp:
    ru = json.load(fp)

with open('translates/pt.json', 'r') as fp:
    pt = json.load(fp)


def add_global_key(key, keys, index, additional_text=''):
    if index > 1 and global_keys[len(global_keys) - 1] == '.'.join(keys):
        global_keys[len(global_keys) - 1] = '.'.join(keys) + '.' + key + additional_text
    else:
        global_keys.append('.'.join(keys) + '.' + key + additional_text)


def comparator(obj1, obj2, index, keys=None):
    for i, key in enumerate(obj1):
        if isinstance(obj1[key], dict):
            if keys is None:
                keys = []
            local_keys = keys[:index]
            if key not in obj2:
                add_global_key(key, local_keys, index)
            elif not isinstance(obj1[key], type(obj2[key])):
                add_global_key(key, local_keys, index, '[diff type]')
            else:
                local_keys.append(key)
                comparator(obj1[key], obj2[key], index + 1, local_keys)
        elif isinstance(obj1[key], list) and key in obj2:
            if len(obj1[key]) != len(obj2[key]):
                add_global_key(key, keys, index, '[diff len]')
        elif (key in obj2) and \
                (isinstance(obj1[key], str) or isinstance(obj1[key], int) or isinstance(obj1[key], bool)) and \
                (isinstance(obj2[key], str) or isinstance(obj2[key], int) or isinstance(obj2[key], bool)):
            pass
        else:
            add_global_key(key, keys, index)


comparator(ru, pt, 0)
for i, key in enumerate(global_keys[1:]):
    if i % 5 == 0 and i > 0:
        print(key + '\n')
    else:
        print(key)
