import os
import re
import csv
import pandas as pd


def write_csv(path, dictionary):
    print(path)
    with open(path, "w", encoding="utf-8") as file:
        for i, v in dictionary.items():
            file.write(f'"{i}","{v}"\n')


def read_file(path):
    with open(path, "r", encoding="utf-8") as file:

        r = file.read().strip('\n').strip('').split("\n")
        res = dict()
        for line in r:
            a = line.split(":")
            print(a)
            res[a[0]] = a[1]

    return res

def read_csv(filename):
    with open(f'{filename}', encoding="utf-8") as file:
        dictishe = dict(csv.reader(file, delimiter=","))
        return dictishe


def process_count_dicts(name, arr, directory):
    dict_s = dict()
    for path in arr:
        if re.search(name, path):
            new_dict = read_file(f"{directory}/{path}")
            for key, value in new_dict.items():
                if not value.isdecimal():
                    continue
                if key not in dict_s.keys():
                    dict_s[key] = 0
                dict_s[key] += int(value)
    dict_s = dict(sorted(dict_s.items(), key=lambda item: item[1], reverse=True))
    print(dict_s)
    write_csv(f"results/joined/{name}.csv", dict_s)


def join_files(name, arr, directory):
    with open(f"results/joined/{name}.csv", "w", encoding="utf-8") as file_joined:
        for path in arr:
            if re.search(name, path):
                with open(f"{directory}/{path}", "r", encoding="utf-8") as file:
                    r = file.read()
                    file_joined.write(r)


def append_to_csv(name, sent1, sent2):
    with open(f"results/joined/separated/symb_{name}.csv", "a", encoding="utf-8") as file:
        sep = "'" if '"' in sent1 else '"'
        file.write(f"{sep}{sent1}{sep},{sep}{sent2}{sep}\n")

def separate_cased():

    long = pd.read_csv("../data/csvs/symbols/symbols_long.csv")
    long = set(long["abbr"])
    short = pd.read_csv("../data/csvs/symbols/symbols.csv")
    short = set(short["abbr"])

    texts = pd.read_csv("results/joined/case_symbols.csv", delimiter=",").reset_index()
    count = 0
    for index, text in texts.iterrows():
        # print(text)

        flag = True
        for l in long:
            if l.lower() in text["question"].lower():
                append_to_csv(l, text["question"], text["answer"])
                flag = False
                count += 1
                break
        if flag:
            for s in short:
                if s in text["question"].lower():
                    append_to_csv(s, text["question"], text["answer"])
                    count += 1
                    break
    print(count)


def join():
    arr_results = os.listdir(f"results/frequency")
    arr_data = os.listdir(f"results/data")
    process_count_dicts("symbols_cased", arr_results, "results/frequency")
    process_count_dicts("symbols_simple_reverse", arr_results, "results/frequency")
    join_files("case_symbols", arr_data, "results/data")

    join_files("simple_symbols", arr_data, "results/data")

    join_files("faulty", arr_data, "results/data")
    print(arr_results)


if __name__ == "__main__":
    separate_cased()
