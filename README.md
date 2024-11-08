# Поиск расстояний до городов

Этот проект реализует скрипт на Python, который вычисляет расстояние и время в пути от списка населенных пунктов до ближайшего крупного города (с населением более 50 000) с использованием API OSRM (Open Source Routing Machine). Результаты сохраняются в Excel-файл для дальнейшего анализа.

## Содержание

- [Функции](#функции)
- [Требования](#требования)
- [Установка](#установка)
- [Использование](#использование)
- [Входные файлы](#входные-файлы)
- [Выходной файл](#выходной-файл)
- [Логирование](#логирование)

## Функции

- Загружает данные из Excel-файлов, содержащих населенные пункты и крупные города (предполалается, что у пользователя есть 2 файла: с координатами всех населенных пунктов и с координатами населенных пунктов с численностью населения более 50000 чел). Расстояние можно отсчитывать и до городов, например, более 100 тыс. чел., тогда нужны координаты только таких населенных пунктов во втором файле.
- Использует API OSRM для расчета расстояний и времени в пути.
- Находит ближайший крупный город для каждого населенного пункта.
- Выводит результаты в новый Excel-файл.

## Требования

Убедитесь, что у вас установлены следующие библиотеки:

- `pandas`
- `numpy`
- `scipy`
- `shapely`
- `requests`
- `openpyxl` (для чтения/записи Excel-файлов)

Вы можете установить эти зависимости с помощью pip:

```bash
pip install pandas numpy scipy shapely requests openpyxl
```
## Установка

Клонируйте этот репозиторий на свой локальный компьютер:

```bash
git clone https://github.com/ваше_имя_пользователя/поиск-расстояний-до-городов.git
```

## Перейдите в директорию проекта:
```bash
cd поиск-расстояний-до-городов
```

## Подготовка входных файлов

Перед запуском скрипта убедитесь, что у вас есть следующие Excel-файлы:

1. **input_file.xlsx**: Этот файл должен содержать все населенные пункты с их ID, широтой, долготой и населением.
   - Структура файла:
     - **id**: Идентификатор населенного пункта (ОКТМО).
     - **latitude**: Широта населенного пункта.
     - **longitude**: Долгота населенного пункта.
     - **population**: Население населенного пункта.

2. **input_file_large.xlsx**: Этот файл должен содержать только крупные города с их ID, широтой и долготой.
   - Структура файла:
     - **id**: Идентификатор крупного города (ОКТМО).
     - **latitude**: Широта города.
     - **longitude**: Долгота города.

## Обновление переменных в скрипте

При необходимости обновите переменные в скрипте:

```python
INPUT_FILE_ALL = "input_file.xlsx"
INPUT_FILE_LARGE = "input_file_large.xlsx"
OUTPUT_FILE = "output_file.xlsx"
```
## Запуск скрипта

Запустите скрипт, используя следующую команду в терминале:

```bash
python поиск_расстояний_до_городов.py
```
# Выходной файл

После завершения работы скрипта будет создан выходной файл:

**output_file.xlsx**: Этот файл будет содержать следующие столбцы:

| Название столбца                       | Описание                                                      |
|----------------------------------------|---------------------------------------------------------------|
| `nearest_large_city_id`               | ID ближайшего крупного города.                               |
| `distance_to_large_city_km`           | Расстояние до ближайшего крупного города в километрах.      |
| `travel_time_to_large_city_min`       | Время в пути до ближайшего крупного города в минутах.       |
