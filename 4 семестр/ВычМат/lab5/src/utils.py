from typing import List, Optional, Tuple

def build_finite_difference_table(y_list: List[float]) -> List[List[float]]:
    """Строит таблицу конечных разностей"""
    table = [list(y_list)]
    prev = table[0]
    while len(prev) > 1:
        row = [prev[i + 1] - prev[i] for i in range(len(prev) - 1)]
        table.append(row)
        prev = row
    return table

def build_divided_difference_table(x_list: List[float], y_list: List[float]) -> List[List[float]]:
    """Строит таблицу разделенных разностей"""
    n = len(x_list)
    table = [[float(y) for y in y_list]]
    prev = table[0]
    for k in range(1, n):
        row = []
        for i in range(n - k):
            row.append((prev[i + 1] - prev[i]) / (x_list[i + k] - x_list[i]))
        table.append(row)
        prev = row
    return table

def check_equidistant(x_list: List[float], eps: float = 1e-9) -> Tuple[bool, Optional[float]]:

    if len(x_list) < 2:
        return False, None
    h = x_list[1] - x_list[0]
    for i in range(1, len(x_list) - 1):
        if abs((x_list[i + 1] - x_list[i]) - h) > eps * max(1.0, abs(h)):
            return False, None
    return True, h

def validate_data(x_list: List[float], y_list: List[float]) -> List[str]:
    """
    Проверяет корректность исходных данных.
    Возвращает список сообщений об ошибках (пустой, если данные корректны).
    """
    errors = []
    if len(x_list) < 2:
        errors.append("Недостаточно точек: необходимо минимум 2 узла.")
    if len(x_list) != len(y_list):
        errors.append("Длины массивов X и Y не совпадают.")
    for i in range(1, len(x_list)):
        if x_list[i] <= x_list[i - 1]:
            errors.append(f"Узлы X должны быть строго возрастающими (нарушение между {x_list[i - 1]} и {x_list[i]}).")
            break
    return errors
