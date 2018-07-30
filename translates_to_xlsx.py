import json
import sys

from openpyxl import Workbook

from json_parser import parse


def translates_to_xlsx(sheet, translates, index=2, grouped=False):
    if grouped:
        for translate, keys in translates.items():
            if len(keys) > 1:
                sheet['B' + str(index)] = '{}'.format(', '.join('.'.join(str(x)) for x in keys))
            else:
                sheet['B' + str(index)] = ".".join([str(x) for x in keys[0]])
                sheet['C' + str(index)] = translate
            index += 1
    else:
        for translate, keys in translates.items():
            if len(keys) > 1:
                for inner_keys in keys:
                    sheet['B' + str(index)] = ".".join([str(x) for x in inner_keys])
                    sheet['C' + str(index)] = translate
                    index += 1
            else:
                sheet['B' + str(index)] = ".".join([str(x) for x in keys[0]])
                sheet['C' + str(index)] = translate
                index += 1


if __name__ == '__main__':
    from_translate, group, to = None, False, 'all.xlsx'
    keys_by_translate = {}

    for i, arg in enumerate(sys.argv):
        if arg == '--from':
            from_translate = sys.argv[i + 1]
        if arg == '--group' and sys.argv[i + 1].lower() == 'true':
            group = True
        if arg == '--to' and sys.argv[i + 1] is not None:
            to = sys.argv[i + 1]

    if from_translate is None:
        raise Exception('''not enough arguments. Should be path to file from''')

    with open(from_translate, 'r') as fp:
        parsed = json.load(fp)
        parse(parsed, [], 0, keys_by_translate)

    global_book = Workbook()

    sheet_local = global_book.active
    sheet_local['C1'] = "Original"
    sheet_local['D1'] = "Translate"

    translates_to_xlsx(sheet_local, keys_by_translate, index=2, grouped=group)

    global_book.save('all.xlsx')
