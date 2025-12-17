
import unittest
import re


class TestTimeRegex(unittest.TestCase):
    #Тестовый класс для проверки функций времени.

    def test_validate_time_correct(self):
        """Проверка корректных времен."""
        correct_times = [
            "00:00:00",
            "12:30:45",
            "23:59:59",
            "01:05:09",
            "1:5:9",      # без ведущих нулей
            "9:30:0",
            "0:0:0",
            "2:15:30",
        ]
        for time_str in correct_times:
            with self.subTest(time=time_str):
                # Импортируем функцию из main
                from main import validate_time
                self.assertTrue(
                    validate_time(time_str),
                    f"Время '{time_str}' должно быть корректным"
                )

    def test_validate_time_incorrect(self):
        #Проверка некорректных времен.
        incorrect_times = [
            "24:00:00",      # час 24 недопустим
            "12:60:00",      # минута 60 недопустима
            "12:30:60",      # секунда 60 недопустима
            "25:15:30",      # час 25 недопустим
            "12:30",         # нет секунд
            "12:30:00:00",   # лишняя часть
            "abc:def:ghi",   # не цифры
            "",              # пустая строка
            " 12:30:45 ",    # пробелы вокруг
            "12.30.45",      # точки вместо двоеточий
            "12:30:45 ",     # пробел в конце
            " 12:30:45",     # пробел в начале
        ]
        for time_str in incorrect_times:
            with self.subTest(time=time_str):
                from main import validate_time
                self.assertFalse(
                    validate_time(time_str),
                    f"Время '{time_str}' должно быть некорректным"
                )

    def test_find_times_in_text_simple(self):
        #Поиск времени в простом тексте
        from main import find_times_in_text
        text = "Встреча в 12:30:45 и 23:59:59."
        found = find_times_in_text(text)
        expected = ["12:30:45", "23:59:59"]
        self.assertEqual(found, expected)

    def test_find_times_in_text_complex(self):
        #Поиск времен в сложном тексте с некорректными данными
        from main import find_times_in_text
        text = """
        Расписание на день:
        08:30:00 - подъем
        09:00:00 - завтрак
        12:60:00 - некорректно (минуты > 59)
        24:00:00 - некорректно (часы > 23)
        13:15:30 - обед
        18:45:00 - ужин
        23:59:59 - конец дня
        """
        found = find_times_in_text(text)
        expected = ["08:30:00", "09:00:00", "13:15:30", "18:45:00", "23:59:59"]
        self.assertEqual(sorted(found), sorted(expected))

    def test_no_times_in_text(self):
        #Текст без времен.
        from main import find_times_in_text
        text = "Это текст без времени, только слова и знаки препинания."
        self.assertEqual(find_times_in_text(text), [])

    def test_boundary_values(self):
        #Проверка граничных значений.
        from main import validate_time
        # Граничные корректные значения
        self.assertTrue(validate_time("00:00:00"))
        self.assertTrue(validate_time("23:59:59"))
        
        # За границами
        self.assertFalse(validate_time("24:00:00"))
        self.assertFalse(validate_time("23:60:00"))
        self.assertFalse(validate_time("23:59:60"))

    def test_leading_zeros_optional(self):
        #Проверка, что ведущие нули не обязательны.
        from main import validate_time
        self.assertTrue(validate_time("01:01:01"))
        self.assertTrue(validate_time("1:1:1"))
        self.assertTrue(validate_time("1:01:01"))
        self.assertTrue(validate_time("01:1:01"))


# Эта функция нужна для запуска тестов из main.py
def run_tests():
    #Запуск тестов и возврат результата.
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestTimeRegex)
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == '__main__':
    # Если запускаем файл напрямую
    unittest.main(verbosity=2)
