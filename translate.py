import json
import sys

from openpyxl import load_workbook

from excel_parser import create_words_dict
from json_parser import parse, switch_keys
from list_to_json import fill_arr, transform_list_to_dict, merge

if __name__ == '__main__':
    from_translate, to_translate, dictionary, log, write_exist = None, None, None, False, False
    for i, arg in enumerate(sys.argv):
        if arg == '--from':
            from_translate = sys.argv[i + 1]
        if arg == '--to':
            to_translate = sys.argv[i + 1]
        if arg == '--dict':
            dictionary = sys.argv[i + 1]
        if arg == '--log':
            log = True
        if arg == '--write-exist':
            write_exist = True
    if from_translate is None or to_translate is None or dictionary is None:
        raise Exception('''not enough arguments.
            should be path to file from, file to and dictionary with translates''')
    keys_by_translate = {}
    with open(from_translate, 'r') as fp:
        parsed = json.load(fp)
        parse(parsed, [], 0, keys_by_translate)
        wb = load_workbook(dictionary)
        wb.close()
        sheet = wb[wb.sheetnames[1]]
        words = create_words_dict(sheet, offset_row=2, column_word_index=1, column_word_offset=1)
        keys_by_translate = switch_keys(keys_by_translate, words, log=log, write_exist=write_exist)

    arr = fill_arr(keys_by_translate)
    arr = transform_list_to_dict(arr)

    cor_obj = arr[0]
    for obj in arr[1:]:
        cor_obj = merge(cor_obj, obj)

    with open(to_translate, 'w') as fp:
        json.dump(cor_obj, fp, ensure_ascii=False, indent=4)
