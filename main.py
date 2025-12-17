"""
Основной модуль для проверки и поиска времени в формате ЧЧ:ММ:СС.
Пользователь может ввести время вручную или загрузить данные из файла.
"""

import re
import unittest
import sys
import os


def validate_time(time_str: str) -> bool:
    """
    Проверяет, является ли строка корректным временем в формате ЧЧ:ММ:СС.

    Правила:
    - Часы: 00–23
    - Минуты: 00–59
    - Секунды: 00–59

    Args:
        time_str (str): Строка для проверки.

    Returns:
        bool: True если время корректно, иначе False.
    """
    pattern = r'^([01]?[0-9]|2[0-3]):([0-5]?[0-9]):([0-5]?[0-9])$'
    return bool(re.match(pattern, time_str))


def find_times_in_text(text: str) -> list:
    """
    Находит все корректные времена в тексте.

    Args:
        text (str): Текст для поиска.

    Returns:
        list: Список найденных корректных времен в формате 'ЧЧ:ММ:СС'.
    """
    pattern = r'\b([01]?[0-9]|2[0-3]):([0-5]?[0-9]):([0-5]?[0-9])\b'
    matches = re.findall(pattern, text)
    # Преобразуем кортежи в строки
    return [':'.join(match) for match in matches]


def user_input_mode():
    """Режим работы с пользовательским вводом."""
    print("\n" + "=" * 40)
    print("Режим проверки времени")
    print("Введите время в формате ЧЧ:ММ:СС")
    print("Или 'exit' для выхода в главное меню")
    print("=" * 40)

    while True:
        user_input = input("\nВведите время: ").strip()
        if user_input.lower() == 'exit':
            break

        if validate_time(user_input):
            print(f"✅ '{user_input}' — корректное время.")
        else:
            print(f"❌ '{user_input}' — некорректное время.")
            print("Примеры корректного времени: 12:30:45, 09:05:00, 23:59:59")


def text_input_mode():
    """Режим поиска времени в тексте."""
    print("\n" + "=" * 40)
    print("Поиск времени в тексте")
    print("Введите текст, а программа найдет все времена ЧЧ:ММ:СС")
    print("=" * 40)

    text = input("\nВведите текст: ").strip()
    times = find_times_in_text(text)
    
    if times:
        print(f"\n✅ Найдено {len(times)} времен:")
        for i, time_str in enumerate(times, 1):
            print(f"  {i}. {time_str}")
    else:
        print("\n❌ Время в формате ЧЧ:ММ:СС не найдено.")


def demo_mode():
    """Демонстрационный режим с примерами."""
    examples = [
        ("12:30:45", True),
        ("23:59:59", True),
        ("00:00:00", True),
        ("24:00:00", False),
        ("12:60:00", False),
        ("09:05:30", True),
        ("9:5:30", True),
        ("1:1:1", True),
        ("12:30", False),
        ("abc:def:ghi", False),
    ]

    print("\n" + "=" * 50)
    print("Демонстрация проверки примеров времени")
    print("=" * 50)

    for time_str, should_be_valid in examples:
        is_valid = validate_time(time_str)
        status = "✅ ПРОШЛО" if is_valid == should_be_valid else "❌ ОШИБКА"
        validity = "Корректно" if is_valid else "Некорректно"
        print(f"{time_str:15} → {validity:15} [{status}]")


def parse_file_for_times(filename: str) -> list:
    """
    Читает файл и находит в нём все корректные времена.
    
    Args:
        filename (str): Имя файла для анализа.
        
    Returns:
        list: Список найденных времен в формате 'ЧЧ:ММ:СС'.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            
        times = find_times_in_text(content)
        return times
        
    except FileNotFoundError:
        print(f"❌ Ошибка: Файл '{filename}' не найден.")
        print("Убедитесь, что файл находится в той же папке, что и программа.")
        return []
    except Exception as e:
        print(f"❌ Ошибка при чтении файла: {e}")
        return []


def file_mode():
    """Режим работы с файлом."""
    print("\n" + "=" * 40)
    print("Поиск времени в файле")
    print("=" * 40)
    
    filename = input("\nВведите имя файла (например, sample.txt): ").strip()
    
    if not filename:
        print("❌ Не указано имя файла.")
        return
    
    times = parse_file_for_times(filename)
    
    if times:
        print(f"\n✅ В файле '{filename}' найдено {len(times)} времен:")
        for i, time_str in enumerate(times, 1):
            print(f"  {i}. {time_str}")
        
        # Сохраняем результат в отдельный файл
        result_filename = f"results_{filename}"
        try:
            with open(result_filename, 'w', encoding='utf-8') as result_file:
                result_file.write(f"Найденные времена в файле '{filename}':\n")
                result_file.write("=" * 40 + "\n")
                for time_str in times:
                    result_file.write(f"{time_str}\n")
            print(f"\n📁 Результаты сохранены в файл: {result_filename}")
        except Exception as e:
            print(f"❌ Не удалось сохранить результаты: {e}")
    else:
        print(f"\n❌ В файле '{filename}' время не найдено.")
        print("Убедитесь, что файл содержит время в формате ЧЧ:ММ:СС.")


def run_tests():
    """Запуск unit-тестов."""
    print("\n" + "=" * 40)
    print("Запуск Unit-тестов")
    print("=" * 40)
    
    try:
        # Импортируем тестовый класс напрямую
        from test_time_regex import TestTimeRegex
        
        # Создаем test suite
        test_suite = unittest.TestLoader().loadTestsFromTestCase(TestTimeRegex)
        
        # Запускаем тесты
        test_runner = unittest.TextTestRunner(verbosity=2)
        result = test_runner.run(test_suite)
        
        # Выводим результаты
        print("\n" + "=" * 40)
        print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
        print("=" * 40)
        print(f"Всего тестов: {result.testsRun}")
        print(f"Провалено: {len(result.failures)}")
        print(f"Ошибок: {len(result.errors)}")
        
        if result.wasSuccessful():
            print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        else:
            print("❌ НЕ ВСЕ ТЕСТЫ ПРОЙДЕНЫ")
            
        # Показываем детали ошибок, если есть
        if result.failures:
            print("\nДетали ошибок:")
            for test, traceback in result.failures:
                print(f"\n❌ {test}:")
                print(traceback)
                
    except ImportError as e:
        print(f"❌ Не удалось импортировать тесты: {e}")
        print("Убедитесь, что файл test_time_regex.py находится в той же папке")
    except Exception as e:
        print(f"❌ Ошибка при запуске тестов: {e}")


def main():
    """Главная функция программы."""
    print("=" * 50)
    print("ЛАБОРАТОРНАЯ РАБОТА: Проверка времени ЧЧ:ММ:СС")
    print("=" * 50)
    print("Автор: [Ваше имя]")
    print("Группа: [Ваша группа]")
    print()

    while True:
        print("\n" + "=" * 30)
        print("ГЛАВНОЕ МЕНЮ")
        print("=" * 30)
        print("1 — Проверить одно время (ввод)")
        print("2 — Найти все времена в тексте")
        print("3 — Поиск времени в файле")
        print("4 — Демонстрация работы")
        print("5 — Запустить unit-тесты")
        print("0 — Выход из программы")
        print("-" * 30)

        choice = input("\nВыберите действие (0-5): ").strip()

        if choice == '1':
            user_input_mode()
        elif choice == '2':
            text_input_mode()
        elif choice == '3':
            file_mode()
        elif choice == '4':
            demo_mode()
        elif choice == '5':
            run_tests()
        elif choice == '0':
            print("\n" + "=" * 30)
            print("Спасибо за использование программы!")
            print("=" * 30)
            break
        else:
            print("❌ Неверный выбор. Пожалуйста, введите число от 0 до 5.")

        input("\nНажмите Enter чтобы продолжить...")


if __name__ == "__main__":
    main()
