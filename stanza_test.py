import re


text = "The Balance of Copyright in Italian National Law (неопр.) // Comparazione e Diritto Civile."

print(re.findall(r"[^\w\s]+", text))


