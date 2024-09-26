import csv


def read_csv(filename):
    with open(f'csvs/{filename}.csv', encoding="utf-8") as file:
        dictishe = dict(csv.reader(file, delimiter=","))
        keys = dictishe.keys()
        return dictishe, keys


def get_symbol(word):
    if word in symbols_keys:
        return symbols[word]
    return word


def has_long_symbol(text):
    for word in symbols_long_keys:
        if word in text:
            text = text.replace(word, symbols_long[word])
    return text


symbols, symbols_keys = read_csv("symbols")
symbols_long, symbols_long_keys = read_csv("symbols_long")

