from DatasetIterator import DatasetIterator

d = DatasetIterator("eBooks")

d.build_index_list()

# Получить общее количество документов в корпусе
print(f"\nОбщее количество документов в корпусе: {d.get_dataset_size()}\n\n")

# Получить документ с определенным docID (все docID – это целые неотрицательные числа)
print(f"Документ с docID = 1000000: {d.get_text_path_by_id(1000000)}\n\n")

# Итератор для получения документов один за другим
print("Первые 10 файлов один за другим, полученные с помощью итератора - метода next():")
i = 0
while i < 10:
    print(f"docID = {i}: {next(d)}")
    i += 1

# Итератор для получения документов в определенном промежутке
print("\nДокументы в промежутке от 100 до 120, полученные с помощью итератора путём заданием параметров - " +
      "вызова статических методов set_start_iter (начальный docID промежутка) и set_limitation (конечный docId промежутка):\n")
d.set_start_iter(100)
d.set_limitation(120)
print("Iteration started")
try:
    while True:
        print(next(d))
except StopIteration:
    print("Iteration stopped\n\n")

# Обычная итерация по всем файлам корпуса (без вызова метода next())
print("Обычная итерация по всем файлам корпуса (без вызова метода next()) - первые 10 файлов один за другим")
d.set_start_iter(0)
d.set_limitation(d.get_dataset_size())
i = 0
for file in d:
    print(f"docID = {i}: {file}")
    i += 1
    if (i == 10):
        break