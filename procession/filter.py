from razdel import tokenize
import csv


with open("../data/csvs/all_measures.txt", "r", encoding="utf-8") as file:
    meas = set(file.read().split("\n"))

with open("../data/csvs/all_sokr.txt", "r", encoding="utf-8") as file:
    sokr = set(file.read().split("\n"))

all_abbr = sokr | meas


def check_sentence(sentence):
    for token in tokenize(sentence):
        word = token.text
        if word in all_abbr:
            return False
    return True


def check_for_measures(sentence):
    for token in tokenize(sentence):
        word = token.text
        if word in meas:
            return True
    return False


def main():
    with open("../data/res/measure_final.csv", "r", encoding="utf-8", newline='') as file:
        text = list(csv.reader(file, delimiter=','))

    file_to_write = open("../data/res/updated/measure.csv", "w", encoding="utf-8")
    for line in text:
        if check_sentence(line[1]):
            # class_sentence = check_for_measures(line[0])
            file_to_write.write(f'"{line[0]}",{line[1]},"measure"\n')

    file_to_write.close()


if __name__ == "__main__":
    main()