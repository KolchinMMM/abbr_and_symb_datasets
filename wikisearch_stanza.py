import stanza
import wikipedia
import warnings
import re
from make_sokr import has_sokr, has_measure, has_long
from wikisearch import write_dict_to_file
import random
from process_symbols import has_long_symbol, get_symbol


def replace_whitespaces(text):
    return re.sub(r"\s+", " ", text)


def update_symbol_dict(sent):
    flag_has = False
    for word in re.findall(r"[^\w\s]+", sent):
        flag_has = True
        if word not in dict_symbols.keys():
            dict_symbols[word] = 0
        dict_symbols[word] += 1
        write_dict_to_file(dict_symbols, f"generated_pairs/symbols_count{generation}.txt", "")
    if flag_has:
        file_sentences_with_symbols.write(sent+"\n")


def get_word_to_add(word):
    word_lower = word.lower()
    sokr = has_sokr(word_lower)
    if sokr:
        if sokr not in dict_res_sokr.keys():
            dict_res_sokr[sokr] = 0
        dict_res_sokr[sokr] += 1
        return sokr

    measure = has_measure(word_lower)
    if measure:
        if measure not in dict_res_measure.keys():
            dict_res_measure[measure] = 0
        dict_res_measure[measure] += 1
        return measure

    return word


dict_res_sokr = dict()
dict_res_measure = dict()
dict_long = dict()
dict_symbols = dict()

generation = "1"

file_abbreviations = open(f"generated_pairs/abbreviations{generation}.csv", "w+", encoding="utf-8")
file_abbreviations.write("question,answer\n")
file_abbreviations.close()

file_symbols = open(f"generated_pairs/symbols{generation}.csv", "w+", encoding="utf-8")
file_symbols.write("question,answer\n")
file_symbols.close()

file_sentences_with_symbols = open(f"generated_pairs/symbols_sentences{generation}.txt", "w", encoding="utf-8")

warnings.catch_warnings()
warnings.simplefilter("ignore")
wikipedia.set_lang("ru")
stanza.download("ru")
nlp = stanza.Pipeline("ru", download_method=None, use_gpu=True)

count_abbr = 0
count_symb = 0

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
                new_sentence_abbr = ""
                new_sentence_symb = ""
                last_index = 0
                for word_token in sentence_tokenized.words:

                    word_to_add_abbr = get_word_to_add(word_token.text)
                    word_to_add_symb = get_symbol(word_token.text)
                    if word_to_add_symb != word_token.text:
                        print(word_to_add_symb)
                    if last_index != word_token.start_char:
                        new_sentence_abbr += " "
                        new_sentence_symb += " "

                    new_sentence_abbr += word_to_add_abbr
                    new_sentence_symb += word_to_add_symb
                    last_index = word_token.end_char

                new_sentence_abbr = replace_whitespaces(new_sentence_abbr.strip())
                new_sentence_symb = replace_whitespaces(new_sentence_symb.strip())
                sentence = replace_whitespaces(sentence).strip()
                update_symbol_dict(sentence)

                another_text = has_long(new_sentence_abbr)
                while another_text:
                    if another_text not in dict_long.keys():
                        dict_long[another_text] = 0
                    dict_long[another_text] += 1
                    new_sentence_abbr = another_text
                    another_text = has_long(another_text)
                another_text_symb = has_long_symbol(new_sentence_symb)

                if new_sentence_abbr != sentence:
                    count_abbr += 1

                    file_abbreviations = open(f"generated_pairs/abbreviations{generation}.csv", "a", encoding="utf-8")
                    file_abbreviations.write(f'"{new_sentence_abbr}","{sentence}"\n')
                    #print("abbr: ", count_abbr)
                if new_sentence_symb != sentence:
                    count_symb += 1
                    print(new_sentence_symb)
                    print(sentence)
                    file_symbols = open(f"generated_pairs/symbols{generation}.csv", "a", encoding="utf-8")
                    file_symbols.write(f'"{new_sentence_symb}","{sentence}"\n')
                    #print("abbr: ", count_symb)
    except:
        write_dict_to_file(dict_res_measure, f"results/measure{generation}.csv", "abbreviation,encounters\n")
        write_dict_to_file(dict_res_sokr, f"results/sokr{generation}.csv", "abbreviation,encounters\n")
        write_dict_to_file(dict_long, f"results/long{generation}.csv", "abbreviation,encounters\n")

        file_abbreviations.close()


