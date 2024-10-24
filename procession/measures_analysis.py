import csv
from search_wiki.make_sokr import read_csv


def print_dict(d):
    for i, v in d.items():
        print(f"{i}\t{v}")


count_prefixes = dict()
count_measures = dict()

prefixes = set(read_csv("prefixes_doli")[0].values()) | set(read_csv("prefixes_kratn")[0].values())
measures = set(read_csv("measures_doli")[0].values()) | set(read_csv("measures_kratn")[0].values())


for measure in measures:
    count_measures[measure] = 0

for prefix in prefixes:
    count_prefixes[prefix] = 0


with open("../data/res/measure_final.csv", "r", encoding="utf-8") as file:
    f = dict(csv.reader(file, delimiter=","))

print(f)

for key, value in f.items():
    print(key, value)
    count = int(value)
    word = key
    if len(word) == 1:
        if word in count_measures:
            count_measures[word] += count
        continue

    for prefix in prefixes:
        if word.startswith(prefix):
            if prefix in count_prefixes:
                count_prefixes[prefix] += count
                word = word[len(prefix):]
                break
    print(word)
    if word in count_measures:
        if word in count_measures:
            count_measures[word] += count
            continue

print_dict(dict(sorted(count_measures.items(), key=lambda item: item[1], reverse=True)))
print("-------------------------------")
print_dict(dict(sorted(count_prefixes.items(), key=lambda item: item[1], reverse=True)))
