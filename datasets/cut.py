import os
import csv
from razdel import tokenize


with open("values_to_remove/sokr.csv", "r", encoding="utf-8") as file:
    sokr = file.read().split("\n")

with open("values_to_remove/measures.csv", "r", encoding="utf-8") as file:
    meas = file.read().split("\n")


dir_name = "small"

for filename in os.listdir(dir_name):
    with open(f"{dir_name}/{filename}", "r", encoding="utf-8") as file:
        res = dict(csv.reader(file, delimiter=','))
        new_file = open(f"{dir_name}_new/{filename}", "w", encoding="utf-8")
        for i, v in res.items():
            flag_halt = False
            for token in tokenize(i):
                word = token.text
                if word in sokr or word in meas:
                    flag_halt = True
            if not flag_halt:
                new_file.write(f'"{i}","{v}"\n')
