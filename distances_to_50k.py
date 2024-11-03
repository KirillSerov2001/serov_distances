import pandas as pd
import numpy as np
from scipy.spatial import Voronoi, cKDTree
from shapely.geometry import Point, Polygon
import requests
import logging
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Конфигурация
INPUT_FILE_ALL = "input_file.xlsx"  # Все населенные пункты
INPUT_FILE_LARGE = "input_file_large.xlsx"  # Населенные пункты более 50 тысяч
OUTPUT_FILE = "output_file.xlsx"  # Имя выходного файла
OSRM_URL = "http://router.project-osrm.org/route/v1/driving/"


def load_data(input_file_all, input_file_large):
    """Загрузка данных из Excel файлов."""
    df_all = pd.read_excel(input_file_all)
    df_large = pd.read_excel(input_file_large)
    return df_all, df_large


def get_osrm_route(origin, destination, osrm_url):
    """Запрос к OSRM для получения расстояния и времени до крупного города."""
    url = f"{osrm_url}{origin[1]},{origin[0]};{destination[1]},{destination[0]}?overview=false"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        route = response.json()
        distance = route['routes'][0]['distance'] / 1000  # В километры
        duration = route['routes'][0]['duration'] / 60  # В минуты
        return distance, duration
    except (requests.RequestException, KeyError) as e:
        logging.error(f"Ошибка OSRM запроса: {e}")
        return None, None


def find_nearest_large_cities(row, large_cities, tree, num_candidates=3):
    """Поиск ближайших крупных городов для заданной точки."""
    if row['population'] >= 50000:
        return row['id'], 0, 0

    point = [row['latitude'], row['longitude']]
    distances, indices = tree.query(point, k=num_candidates)

    nearest_city_id = None
    min_distance = float('inf')
    min_duration = float('inf')

    for idx in indices:
        candidate = large_cities.iloc[idx]
        distance, duration = get_osrm_route((row['latitude'], row['longitude']),
                                            (candidate['latitude'], candidate['longitude']),
                                            OSRM_URL)
        if distance is not None and distance < min_distance:
            min_distance = distance
            min_duration = duration
            nearest_city_id = candidate['id']

    return nearest_city_id, min_distance, min_duration


def save_to_excel(df, results, output_file):
    """Сохранение результатов в Excel файл."""
    df[['nearest_large_city_id', 'distance_to_large_city_km', 'travel_time_to_large_city_min']] = pd.DataFrame(results, index=df.index)
    df.to_excel(output_file, index=False)
    logging.info(f"Результаты сохранены в файл {output_file}")


def main():
    # Загрузка данных
    df_all, df_large = load_data(INPUT_FILE_ALL, INPUT_FILE_LARGE)
    coordinates = df_large[['latitude', 'longitude']].to_numpy()
    tree = cKDTree(coordinates)

    results = []

    # Обработка данных
    for index, row in df_all.iterrows():
        nearest_large_city_id, distance_to_large_city_km, travel_time_to_large_city_min = find_nearest_large_cities(row, df_large, tree)
        results.append([nearest_large_city_id, distance_to_large_city_km, travel_time_to_large_city_min])

        logging.info(f"Обработано {index + 1} строк")

    # Сохранение всех результатов в один файл
    save_to_excel(df_all, results, OUTPUT_FILE)

    logging.info(f"Обработка завершена. Всего обработано {len(df_all)} строк.")


if __name__ == "__main__":
    main()




