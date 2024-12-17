import re

# =, + , - (когда минус), >, <, >=, <=, ==, !=, ~=, ≈ -

symbols = {
    "<=": "меньше или равно",
    ">=": "больше или равно",
    "!=": "не равно",
    "==": "равно",
    "~=": "приблизительно равно",
    "=": "равно",
    "+": "плюс",
    "-": "минус",
    ">": "больше",
    "<": "меньше",
    "≈": "приблизительно равно",
    "~": "приблизительно"
}

data = {
        "температура в -13 градусов" : "температура в минус 13 градусов",
        "+5 градусов за бортом": " плюс 5 градусов за бортом",
        "7 + 3 - 2 равняется 9": "7 плюс 3 минус 2 равняется 9",
        "Сервис disney+": "Сервис disney плюс",
        "выражение 12+7 равно 19": "выражение 12 плюс 7 равно 19",
        "знак на конце-": "знак на конце минус",
        "+": "плюс",
        "в диапазоне 12-15 метров": "в диапазоне 12-15 метров",
        "в пределах двух-трех лет": "в пределах двух-трех лет",
        "в пределах двух - трех лет": "в пределах двух - трех лет",
        "самолет F-35": "самолет F-35"
    }

def is_word(string):
    return string.isalpha()


def endswith(string):
    string_length = len(string)
    for symbol in symbols.keys():
        symbol_length = len(symbol)
        if string_length > symbol_length and string[-symbol_length:] == symbol:
            return symbol
    return False

def startswith(string):
    string_length = len(string)
    for symbol in symbols.keys():
        symbol_length = len(symbol)
        if string_length > symbol_length and string[:symbol_length] == symbol:
            return symbol
    return False


def made_of_symbols(string):
    l = len(string)
    for symbol in symbols.keys():
        if string == symbol*l:
            return symbol
    return False


def replace(text):
    list_text = ["", *re.split("[ \n]", text), ""]
    list_result = []

    placeholder = "{placeholder}" if "{placeholder}" not in text else f"{text}placeholder"
    previous_word = ""
    for index in range(1, len(list_text) - 1):
        current_word = list_text[index]
        next_word = list_text[index + 1]

        # Текущее слово является символом
        if current_word in symbols.keys():
            current_word = symbols[current_word]
        else:
            symb_multiple = made_of_symbols(current_word)
            if symb_multiple:
                list_result.append(current_word)
                continue

            # Проверка символов в начале слова
            symbol_beginning = startswith(current_word)
            words_to_append = ""
            while symbol_beginning:
                # div - не надо
                # if symbol_beginning == "<":
                #     words_to_append += "<"
                #     current_word = current_word[1:]
                #     break
                words_to_append += f"{symbols[symbol_beginning]} "
                current_word = current_word[len(symbol_beginning):]
                symbol_beginning = startswith(current_word)
            current_word = words_to_append + current_word

            # Проверка символов в конце слова
            symbol_end = endswith(current_word)
            words_to_append = ""
            while symbol_end:
                # if symbol_end == ">":
                #     words_to_append += ">"
                #     current_word = current_word[:-1]
                #     break
                words_to_append += f" {symbols[symbol_end]}"
                current_word = current_word[:-len(symbol_end)]
                symbol_end = endswith(current_word)
            current_word = current_word + words_to_append

            # Проверка символов в середине слова
            for symbol in symbols.keys():
                if symbol in current_word.strip(symbol):
                    re_symbol = r"\+" if symbol == "+" else symbol
                    while symbol in current_word:
                        first, second = re.split(re_symbol, current_word, 1)[0:2]
                        # if not is_word(first) and not is_word(second):
                        if symbol != "-":
                            current_word = first.strip() + f" {symbols[symbol]} " + second.strip()
                        else:
                            if first[-1] in [*range(10), *symbols.keys()] and second[0] in [*range(10), *symbols.keys()]:
                                current_word = first.strip() + f" {symbols[symbol]} " + second.strip()
                            else:
                                current_word = current_word.replace("-", placeholder, 1)
            # current_word = current_word.replace(placeholder, "-")
        list_result.append(current_word.replace(placeholder, "-"))
    return " ".join(list_result)


def main():
    while True:
        print(replace(str(input())))



if __name__ == "__main__":
    main()