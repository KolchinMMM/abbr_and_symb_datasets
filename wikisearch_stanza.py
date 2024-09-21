import stanza
import wikipedia
import warnings
import re
from make_sokr import has_sokr, has_measure, is_sokr_itself
from wikisearch import write_dict_to_file


def replace_whitespaces(text):
    return re.sub(r"\s+", " ", text)


def update_symbol_dict(word, sent):
    if len(word) == 1:
        if not re.match(r"[a-zA-Zа-яА-Я0-9.,(){}—-]", word):
            file_sentences_with_symbols.write(f"{sent}\n")
            if word not in dict_symbols.keys():
                dict_symbols[word] = 0
            dict_symbols[word] += 1
            write_dict_to_file(dict_symbols, f"generated_pairs/symbols{generation}.txt", "")


def get_word_to_add(word):
    # if is_sokr_itself(word) or is_sokr_itself(word + "."):
    #     flag_has_abbr = True
    #     file_already_abbr.write(f"{sentence}\n")

    sokr = has_sokr(word)
    if sokr:
        print(sokr)
        if sokr not in dict_res_sokr.keys():
            dict_res_sokr[sokr] = 0
        dict_res_sokr[sokr] += 1
        return sokr

    measure = has_measure(word)
    if measure:
        print(measure)
        if measure not in dict_res_measure.keys():
            dict_res_measure[measure] = 0
        dict_res_measure[measure] += 1
        return measure

    return word


print(replace_whitespaces("\tq   w er t  y"))
exit()

dict_res_sokr = dict()
dict_res_measure = dict()

dict_symbols = dict()

generation = ""

file_abbreviations = open(f"generated_pairs/abbreviations{generation}.csv", "w", encoding="utf-8")
file_abbreviations.write("question,answer\n")
file_already_abbr = open(f"generated_pairs/already_abbr{generation}.txt", "w", encoding="utf-8")
file_sentences_with_symbols = open(f"generated_pairs/symbols_sentences{generation}.txt", "w", encoding="utf-8")

warnings.catch_warnings()
warnings.simplefilter("ignore")
wikipedia.set_lang("ru")
stanza.download("ru")
nlp = stanza.Pipeline("ru", download_method=None)

while True:
    page_title = wikipedia.random()

    page = wikipedia.page(page_title)
    for subsentence in page.content.split("\n"):
        nlpied = nlp(subsentence)
        for sentence_tokenized in nlpied.sentences:
            sentence = sentence_tokenized.text
            new_sentence = ""
            flag_has_abbr = False
            last_index = 0
            for word_token in sentence_tokenized.words:
                update_symbol_dict(word_token.text, sentence)
                word_to_add = get_word_to_add(word_token.text)
                if last_index != word_token.start_char:
                    new_sentence += " "
                new_sentence += word_to_add
                last_index = word_token.end_char
            new_sentence = replace_whitespaces(new_sentence.strip())
            sentence = replace_whitespaces(sentence)
            if new_sentence != sentence and not flag_has_abbr:
                file_abbreviations.write(f'"{new_sentence}","{sentence}"\n')
                print(sentence)
                print(new_sentence)
    # except:
    #     write_dict_to_file(dict_res_measure, f"results/measure{generation}.csv", "abbreviation,encounters\n")
    #     write_dict_to_file(dict_res_sokr, f"results/sokr{generation}.csv", "abbreviation,encounters\n")
    #     file_abbreviations.close()


