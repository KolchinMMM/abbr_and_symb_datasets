from process import read_csv
import stanza
import wikipedia
import warnings
import re


def is_symbol(word):
    for symbol in simple_symbols.keys():
        if word.startswith(symbol):
            return symbol
    return False


def is_written_symbol(word):
    for symbol, text in simple_symbols.items():
        if word == text:
            return symbol
    return False


def is_cased_symbol(word):
    for text, symbol in cased_symbols.items():
        if word == text:
            return symbol


def has_any_cased_symbol(text):
    for symbol in cased_symbols.values():
        if symbol in text:
            return True
    return False


def update_frequency_dict(dictionary, word, path):
    if word not in dictionary.keys():
        dictionary[word] = 0
    dictionary[word] += 1
    with open(path, "w", encoding="utf-8") as file:
        for i, v in dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True)).items():
            file.write(f"{i}:{v}\n")
    return dictionary


def write_end(path, text):
    with open(path, "a", encoding='utf-8') as file:
        file.write(text + "\n")


# read dictionaries
simple_symbols = read_csv("../data/csvs/symbols/simple_symbols.csv")
long_simple_symbols = read_csv("../data/csvs/symbols/simple_symbols_long.csv")
cased_symbols = read_csv("../data/csvs/symbols/symbols.csv")
long_cased_symbols = read_csv("../data/csvs/symbols/symbols_long.csv")


generation = 7
# output for sentence pairs
file_simple_symbols = open(f"results/data/simple_symbols{generation}.csv", "w", encoding="utf-8")
file_simple_symbols.write("question,answer,count_simple,count_simple_translated,count_simple_long,count_simple_long_translated,count_cases_translated,count_cases_long\n")
file_simple_symbols.close()
file_case_symbols = open(f"results/data/case_symbols{generation}.csv", "w", encoding="utf-8")
file_case_symbols.write("question,answer,count_simple,count_simple_translated,count_simple_long,count_simple_long_translated,count_cases_translated,count_cases_long\n")
file_case_symbols.close()

file_faulty = open(f"results/data/faulty{generation}.csv", "w", encoding="utf-8")

# output for frequency dicts
dict_freq_simple = dict()
path_freq_simple = f"results/frequency/symbols_simple{generation}.csv"

dict_freq_simple_reverse = dict()
path_freq_simple_reverse = f"results/frequency/symbols_simple_reverse{generation}.csv"

dict_freq_cased_symbols = dict()
path_freq_cased_symbols = f"results/frequency/symbols_cased{generation}.csv"
stanza.download("ru")
nlp = stanza.Pipeline("ru", download_method=None, use_gpu=True)


def get_pair(text):
    global dict_freq_simple, dict_freq_simple_reverse, dict_freq_cased_symbols

    count_simple = 0
    count_simple_translated = 0
    count_simple_long = 0
    count_simple_long_translated = 0

    count_cases_translated = 0
    count_cases_long = 0

    flag_has_symbol = has_any_cased_symbol(text)
    if flag_has_symbol:
        file_faulty.write(f"{text}\n")
        return False

    list_long = []

    for symbol, long_symbols_written in long_simple_symbols.items():
        reg_symbol = re.compile(re.escape(long_symbols_written), re.IGNORECASE)
        new_text = reg_symbol.sub(symbol, text)
        if new_text != text:
            text = new_text
            count_simple_long_translated += 1
            dict_freq_simple_reverse = update_frequency_dict(dict_freq_simple, symbol, path_freq_simple_reverse)


    for word, symbol in long_cased_symbols.items():
        reg_symbol = re.compile(re.escape(word), re.IGNORECASE)
        new_text = reg_symbol.sub(symbol, text)
        if new_text != text:
            text = new_text
            count_cases_long += 1
            list_long.append(word)

    nlpied = nlp(text)

    for sentence_tokenized in nlpied.sentences:


        sentence_output = ""
        sentence_origin = ""

        last_end_char = 0
        for token in sentence_tokenized.words:
            # Вставка пробелов между словами
            if last_end_char != token.start_char:
                sentence_origin += " "
                sentence_output += " "
            last_end_char = token.end_char

            word = token.text

            # symb = is_symbol(word.lower())
            # if symb:
            #     sentence_origin += word
            #     sentence_output += word.replace(symb, f"{simple_symbols[symb]} ")
            #     dict_freq_simple = update_frequency_dict(dict_freq_simple, symb, path_freq_simple)
            #     count_simple += 1
            #     continue

            symb = is_written_symbol(word.lower())
            if symb:
                sentence_output += word
                sentence_origin += symb
                dict_freq_simple_reverse = update_frequency_dict(dict_freq_simple, symb, path_freq_simple_reverse)
                count_simple_translated += 1
                continue

            symb = is_cased_symbol(word.lower())
            if symb:
                if symb == "°" and "c" in word.lower():
                    continue
                sentence_output += word
                sentence_origin += symb
                dict_freq_cased_symbols = update_frequency_dict(dict_freq_cased_symbols, symb, path_freq_cased_symbols)
                count_cases_translated += 1
                continue

            sentence_origin += word
            sentence_output += word

        for symbol, long_symbols_written in long_simple_symbols.items():
            new_text = sentence_output.replace(symbol, long_symbols_written)
            if new_text != sentence_output:
                sentence_output = new_text
                count_simple_long += 1

        count_simple_long -= count_simple_long_translated

        # for long_cased, symbol in long_cased_symbols.items():
        #     reg_symbol = re.compile(re.escape(long_cased), re.IGNORECASE)
        #     new_text = reg_symbol.sub(symbol, sentence_origin)
        #     if new_text != sentence_origin:
        #         sentence_origin = new_text
        #         count_cases_long += 1

        for elem in list_long:
            sentence_output = sentence_output.replace(long_cased_symbols[elem], elem)
            dict_freq_cased_symbols = update_frequency_dict(dict_freq_cased_symbols, elem, path_freq_cased_symbols)

        keys = (count_simple, count_simple_translated, count_simple_long,
                count_simple_long_translated, count_cases_translated, count_cases_long)
        return sentence_origin.strip(' '), sentence_output.strip(' ').replace("  ", " "), keys


def test():
    texts = [
        "5 >= 4",
        "12 ⩾ 2",
        "555 больше или равно 0",
        "1111 < 41111",
        "Температура -14",
        "10 меньше 43",
        "44 == 4",
        "Выпуск под номером 4",
        "Изделие №62",
        "14 градусов Цельсия",
        "В параграфе 3 указаны",
        "5 долларов",
        "2 фунта стерлингов"

    ]
    texts = ["Натурный лист грузового поезда заполняется согласно форме ДУ-1, пассажирского — ДУ-1Л"]
    for text in texts:
        res = get_pair(text)
        if res:
            sent1, sent2, keys = res
            print(f"{sent1}\n{sent2}\n{keys}")


def main():
    warnings.catch_warnings()
    warnings.simplefilter("ignore")
    wikipedia.set_lang("ru")
    stanza.download("ru")
    count = 0
    while True:
        page_title = wikipedia.random()
        try:
            page = wikipedia.page(page_title)
            for subsentence in page.content.split("\n"):
                if "==" in subsentence:
                    continue
                res = get_pair(subsentence)
                if not res:
                    break
                sent1, sent2, keys = res
                if sent1 != sent2:
                    if '"' in sent1:
                        if "'" in sent1:
                            sent1 = sent1.replace("'", '"')
                            sent2 = sent2.replace("'", '"')
                        to_write = f"'{sent1}','{sent2}',"
                    else:
                        to_write = f'"{sent1}","{sent2}",'
                    to_write += ','.join(list(map(str, keys)))
                    count += 1
                    print(f"{sent1}\n{sent2}\n{count}")
                    if sum(keys[4:]):
                        write_end(f"results/data/case_symbols{generation}.csv", to_write)
                    else:
                        write_end(f"results/data/simple_symbols{generation}.csv", to_write)
        except:
            pass


if __name__ == "__main__":
    main()
