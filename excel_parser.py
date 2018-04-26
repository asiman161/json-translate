def create_words_dict(sheet, offset_row=0, column_word_index=0, column_word_offset=0):
    words_dict = {}

    for i, row in enumerate(sheet.rows):
        if sheet.cell(row=i + offset_row, column=column_word_index).value is not None:
            words_dict[sheet.cell(row=i + offset_row, column=column_word_index).value.strip().lower()] \
                = sheet.cell(row=i + offset_row, column=column_word_index + column_word_offset).value.strip()

    return words_dict


if __name__ == '__main__':
    from openpyxl import load_workbook

    wb = load_workbook('Interface_translate_MN_29.xlsx')
    sheet = wb[wb.sheetnames[0]]

    words = create_words_dict(sheet, offset_row=2, column_word_index=3, column_word_offset=1)
    wb.close()
    print(words)
