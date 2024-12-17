import os
import random
import re


files = os.listdir(f"results/joined/separated")

train = open("datasets/train.csv", "a", encoding="utf-8")
test = open("datasets/test.csv", "a", encoding="utf-8")
valid = open("datasets/valid.csv", "a", encoding="utf-8")

for name in files:
    with open(f"results/joined/separated/{name}", "r", encoding="utf-8") as file:
        res = file.read().split("\n")
    l = len(res)
    count = 0
    random.shuffle(res)

    for i, v in enumerate(res):
        res = re.search(r"([0-9]+)[,.]([0-9]+)", v)
        if res:
            occ = re.findall(res.group(0), v)
            if len(occ) % 2 != 0:
                v = v.replace(res.group(0), f"{res.group(1)} {res.group(2)}")
                print(v)
        if v == "":
            continue
        if i < 0.8 * l:
            train.write(f'{v}\n')
        elif i < 0.9*l:
            valid.write(f"{v}\n")
        else:
            test.write(f"{v}\n")

train.close()
valid.close()
test.close()
