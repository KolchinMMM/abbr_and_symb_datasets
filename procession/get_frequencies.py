import pandas as pd
from procession.filter import meas, sokr
from razdel import tokenize


text = pd.read_csv("../data/res/updated/abbr.csv")


freq_meas = pd.Series([0 for _ in meas], index=meas)
freq_abbr = pd.Series([0 for _ in sokr], index=sokr)


for i in text.iloc:
    for token in tokenize(i["question"]):
        word = token.text
        if word in sokr:
            freq_abbr[word] += 1
        if word in meas:
            freq_meas[word] += 1

f = open("abbr.csv", "w", encoding="utf-8")

for key, val in filter(lambda x: x[0], freq_abbr.sort_values(ascending=False).items()):
    print(key, val)
    f.write(f"{key},{val}\n")


f.close()