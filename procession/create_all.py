from make_sokr import prefixes_doli, prefixes_kratn, measures_with_prefixes, sokr


all_abbr = set()

sokrs = set(sokr.values())
measures = set(measures_with_prefixes.values())
prefixes = set(prefixes_kratn.values()) | set(prefixes_kratn.values())

prefixes.add("")

for prefix in prefixes:
    for measure in measures:
        all_abbr.add(prefix+measure)


with open("../data/csvs/all_measures.txt", "w", encoding="utf-8") as file:
    for s in all_abbr :
        file.write(s.replace("abbreviation", "") + "\n")
