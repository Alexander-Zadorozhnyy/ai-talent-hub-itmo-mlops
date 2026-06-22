import csv


def get_unique_labels(csv_filename):
    """
    Читает CSV-файл с колонками text,label и возвращает set уникальных меток.

    Args:
        csv_filename (str): Путь к CSV-файлу

    Returns:
        set: Множество уникальных меток
    """
    labels = set()

    try:
        with open(csv_filename, "r", encoding="utf-8") as file:
            # Используем csv.DictReader для автоматического определения заголовков
            reader = csv.DictReader(file)

            # Проверяем, что нужные колонки существуют
            if "label" not in reader.fieldnames:
                raise ValueError("В CSV-файле отсутствует колонка 'label'")

            # Собираем все уникальные метки
            for row in reader:
                label = row["label"].strip()
                if label:  # Игнорируем пустые строки
                    labels.add(label)

    except FileNotFoundError:
        print(f"Ошибка: Файл '{csv_filename}' не найден")
        return set()
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return set()

    return labels


# Пример использования
if __name__ == "__main__":
    # Замените на путь к вашему CSV-файлу
    filename = "tmp/train.csv"

    unique_labels = get_unique_labels(filename)

    print(f"Найдено {len(unique_labels)} уникальных меток:")
    print(unique_labels)

    # Для более красивого вывода:
    # print("\nУникальные метки:")
    # for label in sorted(unique_labels):
    #     print(f"  - {label}")
