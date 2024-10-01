import csv
from make_sokr import read_csv

count_prefixes = dict()
count_measures = dict()

prefixes = set(read_csv("prefixes_doli")[0].values()) | set(read_csv("prefixes_kratn")[0].values())
measures = set(read_csv("measures_doli")[0].values()) | set(read_csv("measures_kratn")[0].values())

with open("res/measure_final.csv", "r", encoding="utf-8") as file:
    f = dict(csv.reader(file, delimiter=","))

print(f)

for key, value in f.items():
    print(key, value)
    count = int(value)
    word = key
    if len(word) == 1:
        if word not in count_measures:
            count_measures[word] = 0
        count_measures[word] += count
        continue

    for prefix in prefixes:
        if word.startswith(prefix):
            if prefix not in count_prefixes:
                count_prefixes[prefix] = 0
            count_prefixes[prefix] += count
            word = word[len(prefix):]
            break
    print(word)
    if word in count_measures:
        if word not in count_measures:
            count_measures[word] = 0
        count_measures[word] += count
        continue

print(count_measures)
print(count_prefixes)
