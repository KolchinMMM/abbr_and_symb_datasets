import unittest
from symbols_replacer import replace


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


class TestReplacer(unittest.TestCase):
    def test_plus_minus(self):
        self.assertEqual(replace("температура в -13 градусов"), "температура в минус 13 градусов")
        self.assertEqual(replace("+5 градусов за бортом"), "плюс 5 градусов за бортом")
        self.assertEqual(replace("7 + 3 - 2 равняется 9"), "7 плюс 3 минус 2 равняется 9")
        self.assertEqual(replace("Сервис disney+"), "Сервис disney плюс")
        self.assertEqual(replace("выражение 12+7 равно 19"), "выражение 12 плюс 7 равно 19")
        self.assertEqual(replace("знак на конце-"), "знак на конце минус")
        self.assertEqual(replace("+"), "плюс")
        self.assertEqual(replace("в диапазоне 12-15 метров"), "в диапазоне 12-15 метров")
        self.assertEqual(replace("самолет F-35"), "самолет F-35")
        self.assertEqual(replace("c++"), "c плюс плюс")
        self.assertEqual(replace("++i"), "плюс плюс i")
        self.assertEqual(replace("в районе 12-13 градусов"), "в районе 12-13 градусов")
        self.assertEqual(replace("12 - 13 = -1"), "12 минус 13 равно минус 1")

    def test_greater_less(self):
        self.assertEqual(replace("5 > 4"), "5 больше 4")
        self.assertEqual(replace("19 > 18"), "19 больше 18")
        self.assertEqual(replace("(>90 %)"), "( больше 90 %)")
        self.assertEqual(replace("<"), "меньше")

    def test_equal(self):
        self.assertEqual(replace("RA = 339"), "RA равно 339")
        self.assertEqual(replace("ленты с КНИ=3 %."), "ленты с КНИ равно 3 %.")
        self.assertEqual(replace("уравнение 5x=3"), "уравнение 5x равно 3")
        self.assertEqual(replace("==== Заголовок ===="), "==== Заголовок ====")
        self.assertEqual(replace("param == 5"), "param равно 5")
        self.assertEqual(replace("7 >= 5"), "7 больше или равно 5")
        self.assertEqual(replace("значение <= 5"), "значение меньше или равно 5")
        self.assertEqual(replace("if value != min"), "if value не равно min")
        self.assertEqual(replace("при вероятности~=0.5"), "при вероятности приблизительно равно 0.5")
        self.assertEqual(replace("при вероятности ~=0.5"), "при вероятности приблизительно равно 0.5")
        self.assertEqual(replace("при вероятности~= 0.5"), "при вероятности приблизительно равно 0.5")
        self.assertEqual(replace("="), "равно")
        self.assertEqual(replace("=="), "равно")
        self.assertEqual(replace("b ≈ 5"), "b приблизительно равно 5")

    def test_tilde(self):
        self.assertEqual(replace("240 млрд бел. руб. (~$110 млн.)."), "240 млрд бел. руб. ( приблизительно $110 млн.).")
        self.assertEqual(replace("добавкой фторида калия ~ 6 %"), "добавкой фторида калия приблизительно 6 %")
        self.assertEqual(replace("в ~100 раз больше массы Юпитера"), "в приблизительно 100 раз больше массы Юпитера")
        self.assertEqual(replace("~"), "приблизительно")

    def test_multiple_symbols(self):
        self.assertEqual(replace("5+3=8"), "5 плюс 3 равно 8")


if __name__ == "__main__":
    unittest.main()
