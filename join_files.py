import os
import csv
import re


def read_csv(filename):
    with open(f'generated_pairs/{filename}', encoding="utf-8") as file:
        dictishe = dict(csv.reader(file, delimiter=","))
        return dictishe


def write_csv(path, dictionary):
    with open(path, "a", encoding="utf-8") as file:
        for i, v in dictionary.items():
            file.write(f'"{i}","{v}"\n')



def process(name):
    dict_s = dict()
    for path in arr:
        if re.search(name, path):
            print(directory_path)
            print(path)
            dict_s = dict_s | read_csv(directory_path + path)
    write_csv(f"res/{name}_final.csv", dict_s)


def preprocess(name):
    for path in arr:
        if re.search(name, path):
            with open(f"generated_pairs/{path}", "r", encoding="utf-8") as file:
                buff = file.readlines()
            with open(f"generated_pairs/{path}", "w", encoding="utf-8") as file:
                file.write("question,answer\n")
                for i, v in enumerate(buff):
                    if v.count('"') == 4:
                        file.write(f"{v}")



directory_path = ""
arr = os.listdir(f"generated_pairs")
# preprocess("abbreviations")
process("abbreviations")



