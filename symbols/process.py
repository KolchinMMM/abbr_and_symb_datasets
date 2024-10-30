import csv
import pymorphy2
import stanza

dict_symbols = {
    "№": "номер",
    "°": "градус",
    "§": "параграф",
    "%": "процент",
    "₴": "гривна",
    "$": "доллар",
    "€": "евро",
    "¥": "йена",
    "¥": "юань",
    "₽": "рубль",
}


cases = "nomn gent datv accs ablt loct".split(' ')

forms = "plur femn".split(' ')

morph = pymorphy2.MorphAnalyzer()


def read_csv(filename):
    with open(filename, "r", encoding="utf-8") as file:
        d = dict(csv.reader(file))
    return d


def get_all_forms_2(word1, word2):

    m1 = morph.parse(word1)[0]
    m2 = morph.parse(word2)[0]
    list_res = set()
    for form in forms:
        for case in cases:
            n1 = m1.inflect({form, case})
            n2 = m2.inflect({form, case})
            if n1 and n2:
                list_res.add(f"{n1.word} {n2.word}")
    return list_res


def get_all_forms(word):
    m = morph.parse(word)[0]
    list_res = set()
    for form in forms:
        for case in cases:
            new_word = m.inflect({form, case})
            if new_word:
                list_res.add(new_word.word)
    return list_res


def test_stanza():
    nlp = stanza.Pipeline("ru", download_method=None, use_gpu=True)
    sentence = " в соответствии Законом Амурской области № 382-ОЗ"
    nlpied = nlp(sentence)
    for sentence in nlpied.sentences:
        for word in sentence.words:
            print(word)


def main():
    test_stanza()


if __name__ == "__main__":
    main()