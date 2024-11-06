import os
import random


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
        if v == "":
            continue
        if i < 0.8 * l:
            train.write(f"{v}\n")
        elif i < 0.9*l:
            valid.write(f"{v}\n")
        else:
            test.write(f"{v}\n")

train.close()
valid.close()
test.close()
