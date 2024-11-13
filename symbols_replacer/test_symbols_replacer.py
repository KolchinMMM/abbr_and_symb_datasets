import unittest
from symbols_replacer import replace
# =, + , - (когда минус), >, <, >=, <=, ==, !=, ~=, ≈ -
test_data = {
    "+-": {
        "температура в -13 градусов" : "температура в минус 13 градусов",
        "+5 градусов за бортом": " плюс 5 градусов за бортом",
        "7 + 3 - 2 равняется 9": "7 плюс 3 минус 2 равняется 9",
        "Сервис disney+": "Сервис disney плюс",
        "выражение 12+7 равно 19": "выражение 12 плюс 7 равно 19",
        "знак на конце-": "знак на конце минус",
        "+": "плюс",
        "в диапазоне 12-15 метров": "в диапазоне 12-15 метров",
        "самолет F-35": "самолет F-35"
    }
}

class TestReplacer(unittest.TestCase):
    def test_minus(self):
        for input_text, expected_text in test_data["+-"].items():
            self.assertEqual(replace(input_text), expected_text)