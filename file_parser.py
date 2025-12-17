
import re


def parse_file_for_times(filename: str) -> list:
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()

        pattern = r'\b([01]?[0-9]|2[0-3]):([0-5]?[0-9]):([0-5]?[0-9])\b'
        matches = re.findall(pattern, content)
        
        # Преобразуем кортежи в строки и убираем дубликаты
        times = list(set([':'.join(match) for match in matches]))
        times.sort()  # Сортируем по времени
        
        return times

    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


if __name__ == "__main__":
    # Пример использования
    filename = input("Введите имя файла для анализа: ")
    times = parse_file_for_times(filename)
    
    if times:
        print(f"\nНайдено {len(times)} времен:")
        for time_str in times:
            print(f"  • {time_str}")
    else:
        print("Времена не найдены.")
