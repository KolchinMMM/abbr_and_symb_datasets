from razdel import tokenize
from razdel.segmenters.sentenize import is_sokr

from make_sokr import has_measure, sokr_keys, phds_keys


def create_list_of_abbr(tokens):
    list_correct = []
    for token in tokens:
        word = token.text
        if has_measure(word):
            list_correct.append(word)
            continue
        if word in sokr_keys:
            list_correct.append(word)
    return list_correct


def do(text_correct, text_ans):
    text_correct = text_correct.lower()
    text_ans = text_ans.lower()
    count_all = 0
    count_correct = 0
    list_correct = []
    for long in phds_keys:
        if long in text_correct:
            list_correct.append(long)
            text_correct = text_correct.replace(long, "")
            count_all += 1

    for long in list_correct:
        if long in text_ans:
            count_correct += 1
            text_ans = text_ans.replace(long, "")

    list_correct = create_list_of_abbr(tokenize(text_correct))
    list_ans = create_list_of_abbr(tokenize(text_ans))

    for word in list_correct:
        if word in list_ans:
            count_correct += 1
    return count_correct, count_all + len(list_correct)


def main():
    print(do("Кандидат технических наук В 1987 году Фонд получил нынешнее название.",
             "Кандидат технических наук В 1987 году Фонд получил нынешнее название."))


if __name__ == "__main__":
    main()

