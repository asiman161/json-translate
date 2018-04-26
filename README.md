# Translate generator
### How to use
---
run `python translate.py --from %translate_from.json% --to %translate_to.json% --dict %map_of_translates.xlsx%`

works with only .json and .xlsx files
all arguments are required

example : `python translate.py --from ru.json --to br.json --dict translates.xlsx`

You can use `all-translate.py` or `translate.py`

`all-translate.py` could be outdated and generate wrong data but it only 1 file instead of 4.

### bugs
- doesn't work with arrays
