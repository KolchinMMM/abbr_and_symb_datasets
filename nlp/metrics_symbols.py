import pandas as pd
from razdel import tokenize


symbols = pd.read_csv("../data/csvs/symbols/symbols.csv")
s = pd.Series(list(symbols["abbr"]), index=list(symbols["meaning"]))
long = pd.read_csv("../data/csvs/symbols/symbols_long.csv")
l = pd.Series(list(long["abbr"]), index=list(long["meaning"]))


def get_entrances(text):
    res = dict()
    for i, v in l.items():
        if i in text:
            while i in text:
                if i not in res:
                    res[i] = 0
                res[i] += 1
                text = text.replace(i, "", 1)

    for i, v in s.items():
        if i in text:
            while i in text:
                if i not in res:
                    res[i] = 0
                res[i] += 1
                text = text.replace(i, "", 1)
    return set(res)


def get_metrics(text_correct, text_ans):
    text_correct = text_correct.lower()
    text_ans = text_ans.lower()

    res_initial = get_entrances(text_correct)
    res_answer = get_entrances(text_ans)

    return res_initial, res_answer


def main():
    d_base, d_ans = get_metrics("3 градуса 15 градусов цельсия", "15 градусов цельсия")
    count_all = 0
    count_correct = 0
    print(d_base, d_ans)
    for ind, v in d_base.items():
        count_all += v
        if ind in d_ans.keys():
            count_correct += d_ans[ind]
    print(count_correct, count_all)



if __name__ == "__main__":
    main()
