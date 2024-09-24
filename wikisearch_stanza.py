import stanza
import wikipedia
import warnings
import re
from make_sokr import has_sokr, has_measure, has_long
from wikisearch import write_dict_to_file
import random


def replace_whitespaces(text):
    return re.sub(r"\s+", " ", text)


def update_symbol_dict(sent):
    flag_has = False
    for word in re.findall(r"[^\w\s]+", sent):
        flag_has = True
        if word not in dict_symbols.keys():
            dict_symbols[word] = 0
        dict_symbols[word] += 1
        write_dict_to_file(dict_symbols, f"generated_pairs/symbols{generation}.txt", "")
    if flag_has:
        file_sentences_with_symbols.write(sent)


def get_word_to_add(word):
    word_lower = word.lower()
    sokr = has_sokr(word_lower)
    if sokr:
        print(sokr)
        if sokr not in dict_res_sokr.keys():
            dict_res_sokr[sokr] = 0
        dict_res_sokr[sokr] += 1
        return sokr

    measure = has_measure(word_lower)
    if measure:
        print(measure)
        if measure not in dict_res_measure.keys():
            dict_res_measure[measure] = 0
        dict_res_measure[measure] += 1
        return measure

    return word


dict_res_sokr = dict()
dict_res_measure = dict()
dict_long = dict()
dict_symbols = dict()

generation = "4"

file_abbreviations = open(f"generated_pairs/abbreviations{generation}.csv", "w+", encoding="utf-8")
file_abbreviations.write("question,answer\n")
file_abbreviations.close()

file_already_abbr = open(f"generated_pairs/already_abbr{generation}.txt", "w", encoding="utf-8")
file_sentences_with_symbols = open(f"generated_pairs/symbols_sentences{generation}.txt", "w", encoding="utf-8")

warnings.catch_warnings()
warnings.simplefilter("ignore")
wikipedia.set_lang("ru")
stanza.download("ru")
nlp = stanza.Pipeline("ru", download_method=None, use_gpu=True)

count = 0

while True:
    page_title = wikipedia.random()
    try:
        page = wikipedia.page(page_title)
        for subsentence in page.content.split("\n"):
            if "==" in subsentence:
                continue
            nlpied = nlp(subsentence)
            for sentence_tokenized in nlpied.sentences:

                sentence = sentence_tokenized.text
                new_sentence = ""
                flag_has_abbr = False
                last_index = 0
                for word_token in sentence_tokenized.words:
                    word_to_add = get_word_to_add(word_token.text)
                    if last_index != word_token.start_char:
                        new_sentence += " "
                    new_sentence += word_to_add
                    last_index = word_token.end_char
                new_sentence = replace_whitespaces(new_sentence.strip())
                sentence = replace_whitespaces(sentence)
                update_symbol_dict(sentence)

                another_text = has_long(new_sentence)
                while another_text:
                    if another_text not in dict_long.keys():
                        dict_long[another_text] = 0
                    dict_long[another_text] += 1
                    new_sentence = another_text
                    another_text = has_long(another_text)

                if new_sentence != sentence and not flag_has_abbr:
                    count += 1
                    print(sentence)
                    print(new_sentence)
                    file_abbreviations = open(f"generated_pairs/abbreviations{generation}.csv", "a", encoding="utf-8")
                    file_abbreviations.write(f'"{new_sentence}","{sentence}"\n')
                    print(count)

    except:
        write_dict_to_file(dict_res_measure, f"results/measure{generation}.csv", "abbreviation,encounters\n")
        write_dict_to_file(dict_res_sokr, f"results/sokr{generation}.csv", "abbreviation,encounters\n")
        write_dict_to_file(dict_long, f"results/long{generation}.csv", "abbreviation,encounters\n")
        file_abbreviations.close()


