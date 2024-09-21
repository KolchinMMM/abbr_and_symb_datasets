import wikipedia
import warnings
import razdel
from make_sokr import has_sokr, has_measure, is_sokr_itself


def write_dict_to_file(dictionary, path, header):
    sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
    with open(path, "w", encoding="utf-8") as file:
        file.write(header)
        for i, v in sorted_dict.items():
            file.write(f"{i},{v}\n")


def main():
    warnings.catch_warnings()
    warnings.simplefilter("ignore")
    wikipedia.set_lang("ru")

    dict_res_sokr = dict()
    dict_res_measure = dict()
    generation = ""

    file_abbreviations = open(f"generated_pairs/abbreviations{generation}.csv", "w", encoding="utf-8")
    file_abbreviations.write("question,answer\n")
    file_already_abbr = open(f"generated_pairs/already_abbr{generation}.txt", "w", encoding="utf-8")
    while True:
        page_title = wikipedia.random()
        try:
            page = wikipedia.page(page_title)
            for sentence1 in razdel.sentenize(page.content):
                for sentence in sentence1.text.split("\n"):
                    new_sentence = []
                    flag_has_abbr = False
                    print(sentence)
                    for word_token in razdel.tokenize(sentence):
                        print(word_token)
                        word = word_token.text
                        if is_sokr_itself(word) or is_sokr_itself(word+"."):
                            flag_has_abbr = True
                            file_already_abbr.write(f"{sentence}\n")
                            break
                        sokr = has_sokr(word)
                        if sokr:
                            print(sokr)
                            new_sentence = new_sentence.append(sokr)
                            if sokr not in dict_res_sokr.keys():
                                dict_res_sokr[sokr] = 0
                            dict_res_sokr[sokr] += 1
                            break
                        measure = has_measure(word)
                        if measure:
                            print(measure)
                            new_sentence = new_sentence.append(sokr)
                            if measure in dict_res_measure.keys():
                                dict_res_measure[measure] = 0
                            dict_res_measure[measure] += 1
                            break
                    if new_sentence != sentence and not flag_has_abbr:
                        print("Пошло добро")
                        file_abbreviations.write(f'"{new_sentence}","{sentence}"\n')
        except:
            write_dict_to_file(dict_res_measure, f"results/measure{generation}.csv", "abbreviation,encounters\n")
            write_dict_to_file(dict_res_sokr, f"results/sokr{generation}.csv", "abbreviation,encounters\n")
            file_abbreviations.close()

if __name__ == "__main__":
    main()