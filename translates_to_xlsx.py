import json
import sys

from openpyxl import Workbook

from json_parser import parse


def translates_to_xlsx(sheet, translates, index=2, grouped=False):
    """все ключи хранятся в массиве string[][], например: [['HOME', 'SELECT'], ['HOME', 'ERROR']]"""
    if grouped:
        for translate, keys in translates.items():
            if len(keys) > 1:
                """[['HOME', 'SELECT'], ['HOME', 'ERROR']] > 'HOME.SELECT, HOME.ERROR'"""
                # Если произойдет ошибка int > str, то сделать поменять строку на
                # sheet['B' + str(index)] = '{}'.format(', '.join('.'.join(x) for x in keys))
                sheet['B' + str(index)] = '{}'.format(', '.join('.'.join(x) for x in keys))
            else:
                """['HOME', 'SELECT']] > 'HOME.SELECT'"""
                sheet['B' + str(index)] = ".".join([str(x) for x in keys[0]])
                sheet['C' + str(index)] = translate
            index += 1
    else:
        for translate, keys in translates.items():
            if len(keys) > 1:
                for inner_keys in keys:
                    """['HOME', 'SELECT']] > 'HOME.SELECT'"""
                    sheet['B' + str(index)] = ".".join([str(x) for x in inner_keys])
                    sheet['C' + str(index)] = translate
                    index += 1
            else:
                """['HOME', 'SELECT']] > 'HOME.SELECT'"""
                sheet['B' + str(index)] = ".".join([str(x) for x in keys[0]])
                sheet['C' + str(index)] = translate
                index += 1


if __name__ == '__main__':
    from_translate, group, to = None, False, 'all.xlsx'
    keys_by_translate = {}

    for i, arg in enumerate(sys.argv):
        """Откуда брать переводы. Указывается адрес JSON файла"""
        if arg == '--from':
            from_translate = sys.argv[i + 1]
        """Группировать ли переводы. У одного перевода будет несколько ключей"""
        if arg == '--group':
            group = True
        """Имя файла, в котором надо все сохранить"""
        if arg == '--to' and sys.argv[i + 1] is not None:
            to = sys.argv[i + 1]

    if from_translate is None:
        raise Exception('''not enough arguments. Should be path to file from''')

    with open(from_translate, 'r') as fp:
        parsed = json.load(fp)
        parse(parsed, [], 0, keys_by_translate)

    global_book = Workbook()

    sheet_local = global_book.active
    sheet_local['B1'] = "Ключи"
    sheet_local['C1'] = "Переводы"

    translates_to_xlsx(sheet_local, keys_by_translate, index=2, grouped=group)

    global_book.save(to)
