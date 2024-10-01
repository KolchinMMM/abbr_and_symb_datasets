import csv
import re


def read_csv(filename):
    with open(f'csvs/{filename}.csv', encoding="utf-8") as file:
        dictishe = dict(csv.reader(file, delimiter=","))
        keys = dictishe.keys()
        return dictishe, keys


def is_composit_sokr(word, list_measure, list_prefix):
    for prefix in list_prefix:
        if word.startswith(prefix):
            return word.replace(prefix, "") in list_measure
    return False


def is_sokr_itself(word):
    return (word in measures.values()
            or word in sokr.values()
            or is_composit_sokr(word, measures_with_prefixes.values(), prefixes_doli.values())
            or is_composit_sokr(word, measures_with_prefixes.values(), prefixes_kratn.values()))


def has_sokr(word):
    return sokr[word] if word in sokr_keys else ""


def has_measure(word):
    doli = has_measure_with_prefix(word, prefixes_doli, prefixes_doli_keys, measures_with_prefixes, measures_with_prefixes_keys)
    if doli:
        return doli
    kratn = has_measure_with_prefix(word, prefixes_kratn, prefixes_kratn_keys, measures_with_prefixes, measures_with_prefixes_keys)
    if kratn:
        return kratn
    if word in measures_keys:
        return measures[word]
    return ""


def has_measure_with_prefix(word, prefix_dict, prefix_keys, measure_dict, measure_keys):
    first_half = ""
    first_half_translated = ""
    for prefix in prefix_keys:
        if re.match(f'^{prefix}.+', word):
            first_half = prefix
            first_half_translated = prefix_dict[first_half]
    word = word.replace(first_half, "")
    for measure in measure_keys:
        if measure == word:
            return first_half_translated + measure_dict[measure]

    return ""


def has_long(text):
    for line in phds_keys:
        if line in text:
            return text.replace(line, phds[line])
    return ""


sokr, sokr_keys = read_csv("sokr")
measures, measures_keys = read_csv("measures")
measures_with_prefixes, measures_with_prefixes_keys = read_csv("measures_with_prefixes")
phds, phds_keys = read_csv("phds")
prefixes_doli, prefixes_doli_keys = read_csv("prefixes_doli")
prefixes_kratn, prefixes_kratn_keys = read_csv("prefixes_kratn")


def main():
    print(has_measure("микробеккерелей"))




if __name__ == "__main__":
    main()


