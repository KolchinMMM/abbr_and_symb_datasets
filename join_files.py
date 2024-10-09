import os
import csv
import re
import random


def read_csv(filename):
    with open(f'{filename}', encoding="utf-8") as file:
        dictishe = dict(csv.reader(file, delimiter=","))
        return dictishe


def read_text(filename):
    with open(f"generated_pairs/{filename}", "r", encoding="utf8",) as file:
        f = file.readlines()
        for i in f:
            a, b = i.rsplit(",")
            print(a, b)


def write_csv(path, dictionary):
    with open(path, "a", encoding="utf-8") as file:
        for i, v in dictionary.items():
            file.write(f'"{i}","{v}"\n')


def process(name, arr, directory):
    dict_s = dict()
    for path in arr:
        if re.search(name, path):
            dict_s = dict_s | read_csv(directory + path)
    write_csv(f"res/{name}_final.csv", dict_s)


def process_count_dicts(name, arr, directory):
    dict_s = dict()
    for path in arr:
        if re.search(name, path):
            new_dict = read_csv(f"{directory}/{path}")
            for key, value in new_dict.items():
                if not value.isdecimal():
                    continue
                if key not in dict_s.keys():
                    dict_s[key] = 0
                print(key, value)
                dict_s[key] += int(value)
    dict_s = dict(sorted(dict_s.items(), key=lambda item: item[1], reverse=True))
    write_csv(f"res/frequency/{name}.csv", dict_s)


def preprocess(name, arr):
    for path in arr:
        if re.search(name, path):
            with open(f"generated_pairs/{path}", "r", encoding="utf-8") as file:
                buff = file.readlines()
            with open(f"generated_pairs/{path}", "w", encoding="utf-8") as file:
                file.write("question,answer\n")
                for i, v in enumerate(buff):
                    if v.count('"') == 4:
                        file.write(f"{v.replace('..', '.')}")


def join_and_shuffle():
    d = read_csv("res/measure_final.csv")
    abbr = read_csv("res/abbreviation_final.csv")
    count = 0
    for i, v in abbr.items():
        count += 1
        d[i] = v
        if count > 60000:
            break
    print(len(d))
    d = list(d.items())
    random.shuffle(d)
    shuffled = dict(d)
    write_csv("res/dataset1.csv", shuffled)


directory_path = ""
arr_generated_pairs = os.listdir(f"generated_pairs")
arr_results = os.listdir(f"results")
# preprocess("measure", arr_generated_pairs)

#process("abbreviation", arr_generated_pairs, "generated_pairs/")

# process_count_dicts("measure", arr_results, "results")

join_and_shuffle()


