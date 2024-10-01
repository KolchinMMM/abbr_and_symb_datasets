import csv
from make_sokr import read_csv

count_prefixes = dict()
count_measures = dict()

prefixes = read_csv("prefixes_doli").values() | read_csv("prefixes_doli").values()


with open("res/measure_final.csv", "r", encoding="utf-8") as file:
    f = dict(csv.reader(file, delimiter=","))

for key, value in f.items():
    word = key
    if len(word) == 1:
        if word not in count_measures:
            count_measures[word] = 0
        count_measures[word] += value
        break

    for prefix in prefixes:
        if word.startswith(prefix):
            if word not in count_prefixes:
                count_prefixes[word] = 0
            count_prefixes[word] += value
            word = word[len(prefix):]
            break

    if word in count_measures:
        if word not in count_measures:
            count_measures[word] = 0
        count_measures[word] += value
        break

