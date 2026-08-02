# methods.py
import math
from typing import List, Optional

from data import InterpolationResult
from utils import (build_divided_difference_table, build_finite_difference_table,
                   check_equidistant)

# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------

def _nearest_index(x: float, x_list: List[float]) -> int:
    """Возвращает индекс узла, ближайшего к x."""
    return min(range(len(x_list)), key=lambda i: abs(x_list[i] - x))

def _left_index(x: float, x_list: List[float]) -> int:
    """Возвращает индекс наибольшего узла, не превосходящего x."""
    idx = 0
    for i in range(len(x_list)):
        if x_list[i] <= x:
            idx = i
    return idx

def _right_index(x: float, x_list: List[float]) -> int:
    """Возвращает индекс наименьшего узла, не меньшего x."""
    for i in range(len(x_list)):
        if x_list[i] >= x:
            return i
    return len(x_list) - 1

def _falling_product(t: float, start: int, end: int) -> float:
    """Произведение (t - r) для r от start до end включительно."""
    prod = 1.0
    for r in range(start, end + 1):
        prod *= (t - r)
    return prod

def _in_range(table, k: int, i: int) -> bool:
    """Проверяет, что элемент table[k][i] существует."""
    return 0 <= k < len(table) and 0 <= i < len(table[k])

# ---------------------------------------------------------------------------
# Многочлен Лагранжа
# ---------------------------------------------------------------------------

def lagrange_interpolation(x: float, x_list: List[float], y_list: List[float]) -> InterpolationResult:
    """Интерполяционный многочлен Лагранжа, построенный по всем узлам."""
    name = "Многочлен Лагранжа"
    try:
        n = len(x_list)
        value = 0.0
        for i in range(n):
            li = 1.0
            for j in range(n):
                if i != j:
                    li *= (x - x_list[j]) / (x_list[i] - x_list[j])
            value += y_list[i] * li
        return InterpolationResult(name, x, value, "Успешно")
    except Exception as e:
        return InterpolationResult(name, x, None, f"Ошибка: {e}")

# ---------------------------------------------------------------------------
# Многочлен Ньютона с разделенными разностями
# ---------------------------------------------------------------------------

def newton_divided_forward(x: float, x_list: List[float], y_list: List[float]) -> InterpolationResult:
    """
    Первая интерполяционная формула Ньютона с разделенными разностями
    (интерполирование вперед, от узла x0).
    """
    name = "Ньютон (разделенные разности), 1-я формула"
    try:
        table = build_divided_difference_table(x_list, y_list)
        n = len(x_list)
        value = table[0][0]
        term = 1.0
        for k in range(1, n):
            term *= (x - x_list[k - 1])
            value += table[k][0] * term
        return InterpolationResult(name, x, value, "Успешно",
                                   formula="Интерполирование вперед (от x0)")
    except Exception as e:
        return InterpolationResult(name, x, None, f"Ошибка: {e}")

def newton_divided_backward(x: float, x_list: List[float], y_list: List[float]) -> InterpolationResult:
    """
    Вторая интерполяционная формула Ньютона с разделенными разностями
    (интерполирование назад, от узла xn).
    """
    name = "Ньютон (разделенные разности), 2-я формула"
    try:
        table = build_divided_difference_table(x_list, y_list)
        n = len(x_list)
        value = table[0][n - 1]
        term = 1.0
        for k in range(1, n):
            term *= (x - x_list[n - k])
            value += table[k][n - 1 - k] * term
        return InterpolationResult(name, x, value, "Успешно",
                                   formula="Интерполирование назад (от xn)")
    except Exception as e:
        return InterpolationResult(name, x, None, f"Ошибка: {e}")

def newton_divided(x: float, x_list: List[float], y_list: List[float]) -> InterpolationResult:
    """Ньютон с разделенными разностями: 1-я формула для левой половины отрезка, 2-я — для правой."""
    name = "Ньютон (разделенные разности)"
    try:
        mid = (x_list[0] + x_list[-1]) / 2.0
        if x <= mid:
            return newton_divided_forward(x, x_list, y_list)
        return newton_divided_backward(x, x_list, y_list)
    except Exception as e:
        return InterpolationResult(name, x, None, f"Ошибка: {e}")

# ---------------------------------------------------------------------------
# Многочлен Ньютона с конечными разностями (равноотстоящие узлы)
# ---------------------------------------------------------------------------

def newton_finite_forward(x: float, x_list: List[float], y_list: List[float]) -> InterpolationResult:
    """
    Первая интерполяционная формула Ньютона с конечными разностями
    (интерполирование вперед). Используется для левой половины отрезка.
    """
    name = "Ньютон (конечные разности), 1-я формула"
    try:
        ok, h = check_equidistant(x_list)
        if not ok:
            return InterpolationResult(name, x, None,
                                       "Неприменимо: узлы не равноотстоящие")
        table = build_finite_difference_table(y_list)
        n = len(x_list)
        t = (x - x_list[0]) / h
        value = table[0][0]
        fact = 1.0
        prod = 1.0
        for k in range(1, n):
            prod *= (t - (k - 1))
            fact *= k
            value += table[k][0] * prod / fact
        return InterpolationResult(name, x, value, "Успешно",
                                   formula=f"Интерполирование вперед, t = (x - x0)/h = {t:.4f}")
    except Exception as e:
        return InterpolationResult(name, x, None, f"Ошибка: {e}")

def newton_finite_backward(x: float, x_list: List[float], y_list: List[float]) -> InterpolationResult:
    """
    Вторая интерполяционная формула Ньютона с конечными разностями
    (интерполирование назад). Используется для правой половины отрезка.
    """
    name = "Ньютон (конечные разности), 2-я формула"
    try:
        ok, h = check_equidistant(x_list)
        if not ok:
            return InterpolationResult(name, x, None,
                                       "Неприменимо: узлы не равноотстоящие")
        table = build_finite_difference_table(y_list)
        n = len(x_list)
        t = (x - x_list[n - 1]) / h
        value = table[0][n - 1]
        fact = 1.0
        prod = 1.0
        for k in range(1, n):
            prod *= (t + (k - 1))
            fact *= k
            value += table[k][n - 1 - k] * prod / fact
        return InterpolationResult(name, x, value, "Успешно",
                                   formula=f"Интерполирование назад, t = (x - xn)/h = {t:.4f}")
    except Exception as e:
        return InterpolationResult(name, x, None, f"Ошибка: {e}")

def newton_finite(x: float, x_list: List[float], y_list: List[float]) -> InterpolationResult:
    """Ньютон с конечными разностями: 1-я формула для левой половины отрезка, 2-я — для правой."""
    name = "Ньютон (конечные разности)"
    try:
        mid = (x_list[0] + x_list[-1]) / 2.0
        if x <= mid:
            return newton_finite_forward(x, x_list, y_list)
        return newton_finite_backward(x, x_list, y_list)
    except Exception as e:
        return InterpolationResult(name, x, None, f"Ошибка: {e}")

# ---------------------------------------------------------------------------
# Многочлен Гаусса (равноотстоящие узлы, интерполирование в середине таблицы)
# ---------------------------------------------------------------------------

def _gauss_first_value(x: float, x_list: List[float], y_list: List[float],
                       table: List[List[float]], c: int) -> float:
    """
    Первая интерполяционная формула Гаусса с центральным узлом x[c].
    Применяется для x > a (t >= 0).
    """
    n = len(x_list)
    h = x_list[1] - x_list[0]
    t = (x - x_list[c]) / h
    value = y_list[c]
    if _in_range(table, 1, c):
        value += t * table[1][c]
    m = 1
    while True:
        k_even = 2 * m
        k_odd = 2 * m + 1
        any_added = False
        if _in_range(table, k_even, c - m):
            factor = _falling_product(t, -(m - 1), m)
            value += table[k_even][c - m] * factor / math.factorial(k_even)
            any_added = True
        if _in_range(table, k_odd, c - m):
            factor = _falling_product(t, -m, m)
            value += table[k_odd][c - m] * factor / math.factorial(k_odd)
            any_added = True
        if not any_added:
            break
        m += 1
    return value

def _gauss_second_value(x: float, x_list: List[float], y_list: List[float],
                        table: List[List[float]], c: int) -> float:
    """
    Вторая интерполяционная формула Гаусса с центральным узлом x[c].
    Применяется для x < a (t <= 0).
    """
    n = len(x_list)
    h = x_list[1] - x_list[0]
    t = (x - x_list[c]) / h
    value = y_list[c]
    if _in_range(table, 1, c - 1):
        value += t * table[1][c - 1]
    m = 1
    while True:
        k_even = 2 * m
        k_odd = 2 * m + 1
        any_added = False
        if _in_range(table, k_even, c - m):
            factor = _falling_product(t, -m, m - 1)
            value += table[k_even][c - m] * factor / math.factorial(k_even)
            any_added = True
        if _in_range(table, k_odd, c - (m + 1)):
            factor = _falling_product(t, -m, m)
            value += table[k_odd][c - (m + 1)] * factor / math.factorial(k_odd)
            any_added = True
        if not any_added:
            break
        m += 1
    return value

def gauss_first(x: float, x_list: List[float], y_list: List[float]) -> InterpolationResult:
    """Первая интерполяционная формула Гаусса (интерполирование вперед)."""
    name = "Гаусс, 1-я формула"
    try:
        ok, h = check_equidistant(x_list)
        if not ok:
            return InterpolationResult(name, x, None, "Неприменимо: узлы не равноотстоящие")
        n = len(x_list)
        c = _left_index(x, x_list)
        if c >= n - 1:
            c = n - 2
        t = (x - x_list[c]) / h
        table = build_finite_difference_table(y_list)
        value = _gauss_first_value(x, x_list, y_list, table, c)
        return InterpolationResult(name, x, value, "Успешно",
                                   formula=f"Центральный узел x[{c}] = {x_list[c]}, t = {t:.4f}")
    except Exception as e:
        return InterpolationResult(name, x, None, f"Ошибка: {e}")

def gauss_second(x: float, x_list: List[float], y_list: List[float]) -> InterpolationResult:
    """Вторая интерполяционная формула Гаусса (интерполирование назад)."""
    name = "Гаусс, 2-я формула"
    try:
        ok, h = check_equidistant(x_list)
        if not ok:
            return InterpolationResult(name, x, None, "Неприменимо: узлы не равноотстоящие")
        n = len(x_list)
        c = _right_index(x, x_list)
        if c < 1:
            c = 1
        t = (x - x_list[c]) / h
        table = build_finite_difference_table(y_list)
        value = _gauss_second_value(x, x_list, y_list, table, c)
        return InterpolationResult(name, x, value, "Успешно",
                                   formula=f"Центральный узел x[{c}] = {x_list[c]}, t = {t:.4f}")
    except Exception as e:
        return InterpolationResult(name, x, None, f"Ошибка: {e}")

def gauss(x: float, x_list: List[float], y_list: List[float]) -> InterpolationResult:
    """Гаусс: автоматический выбор первой или второй формулы относительно ближайшего узла."""
    name = "Гаусс (автовыбор)"
    try:
        ok, h = check_equidistant(x_list)
        if not ok:
            return InterpolationResult(name, x, None, "Неприменимо: узлы не равноотстоящие")
        n = len(x_list)
        c = _nearest_index(x, x_list)
        t = (x - x_list[c]) / h
        table = build_finite_difference_table(y_list)
        if t >= 0:
            c = min(c, n - 2)
            value = _gauss_first_value(x, x_list, y_list, table, c)
            note = f"1-я формула, центральный узел x[{c}] = {x_list[c]}"
        else:
            c = max(c, 1)
            value = _gauss_second_value(x, x_list, y_list, table, c)
            note = f"2-я формула, центральный узел x[{c}] = {x_list[c]}"
        return InterpolationResult(name, x, value, "Успешно", formula=note)
    except Exception as e:
        return InterpolationResult(name, x, None, f"Ошибка: {e}")

# ---------------------------------------------------------------------------
# Схема Стирлинга (необязательное задание, |t| <= 0.25)
# ---------------------------------------------------------------------------

def stirling(x: float, x_list: List[float], y_list: List[float]) -> InterpolationResult:
    """Интерполяционная формула Стирлинга (интерполирование при малых |t| <= 0.25)."""
    name = "Стирлинг"
    try:
        ok, h = check_equidistant(x_list)
        if not ok:
            return InterpolationResult(name, x, None, "Неприменимо: узлы не равноотстоящие")
        n = len(x_list)
        c = _nearest_index(x, x_list)
        t = (x - x_list[c]) / h
        if abs(t) > 0.25 + 1e-9:
            return InterpolationResult(name, x, None, "Неприменимо: |t| > 0.25 (формула применима при малых t)",
                                       formula=f"Ближайший узел x[{c}] = {x_list[c]}, t = {t:.4f}")
        table = build_finite_difference_table(y_list)
        value = y_list[c]
        if _in_range(table, 1, c - 1) and _in_range(table, 1, c):
            value += t * (table[1][c - 1] + table[1][c]) / 2.0
        if _in_range(table, 2, c - 1):
            value += t * t / 2.0 * table[2][c - 1]
        m = 1
        while True:
            k_odd = 2 * m + 1
            k_even = 2 * m + 2
            any_added = False
            if _in_range(table, k_odd, c - m - 1) and _in_range(table, k_odd, c - m):
                prod = 1.0
                for r in range(1, m + 1):
                    prod *= (t * t - r * r)
                factor = t * prod / math.factorial(k_odd)
                value += factor * (table[k_odd][c - m - 1] + table[k_odd][c - m]) / 2.0
                any_added = True
            if _in_range(table, k_even, c - m - 1):
                prod = 1.0
                for r in range(1, m + 1):
                    prod *= (t * t - r * r)
                value += table[k_even][c - m - 1] * t * t * prod / math.factorial(k_even)
                any_added = True
            if not any_added:
                break
            m += 1
        return InterpolationResult(name, x, value, "Успешно",
                                   formula=f"Центральный узел x[{c}] = {x_list[c]}, t = {t:.4f}")
    except Exception as e:
        return InterpolationResult(name, x, None, f"Ошибка: {e}")

# ---------------------------------------------------------------------------
# Схема Бесселя (необязательное задание, 0.25 <= t <= 0.75)
# ---------------------------------------------------------------------------

def bessel(x: float, x_list: List[float], y_list: List[float]) -> InterpolationResult:
    """Интерполяционная формула Бесселя (интерполирование при 0.25 <= t <= 0.75)."""
    name = "Бессель"
    try:
        ok, h = check_equidistant(x_list)
        if not ok:
            return InterpolationResult(name, x, None, "Неприменимо: узлы не равноотстоящие")
        n = len(x_list)
        c = _left_index(x, x_list)
        if c >= n - 1:
            c = n - 2
        t = (x - x_list[c]) / h
        if not (0.25 - 1e-9 <= t <= 0.75 + 1e-9):
            return InterpolationResult(name, x, None, "Неприменимо: t вне [0.25; 0.75]",
                                       formula=f"Узел x[{c}] = {x_list[c]}, t = {t:.4f}")
        table = build_finite_difference_table(y_list)
        value = (y_list[c] + y_list[c + 1]) / 2.0
        if _in_range(table, 1, c):
            value += (t - 0.5) * table[1][c]
        m = 1
        while True:
            k_even = 2 * m
            k_odd = 2 * m + 1
            any_added = False
            if _in_range(table, k_even, c - m) and _in_range(table, k_even, c - m + 1):
                prod = 1.0
                for r in range(1, m):
                    prod *= (t + r) * (t - r - 1)
                factor = t * (t - 1) * prod / math.factorial(k_even)
                value += factor * (table[k_even][c - m] + table[k_even][c - m + 1]) / 2.0
                any_added = True
            if _in_range(table, k_odd, c - m):
                prod = 1.0
                for r in range(1, m):
                    prod *= (t + r) * (t - r - 1)
                factor = (t - 0.5) * t * (t - 1) * prod / math.factorial(k_odd)
                value += table[k_odd][c - m] * factor
                any_added = True
            if not any_added:
                break
            m += 1
        return InterpolationResult(name, x, value, "Успешно",
                                   formula=f"Узел x[{c}] = {x_list[c]}, t = {t:.4f}")
    except Exception as e:
        return InterpolationResult(name, x, None, f"Ошибка: {e}")

# ---------------------------------------------------------------------------
# Список всех методов для таблицы сравнения
# ---------------------------------------------------------------------------

def all_methods() -> List[dict]:
    """Возвращает описание всех методов для отображения в интерфейсе."""
    return [
        {"name": "Многочлен Лагранжа", "func": lagrange_interpolation},
        {"name": "Ньютон (разделенные разности), 1-я формула", "func": newton_divided_forward},
        {"name": "Ньютон (разделенные разности), 2-я формула", "func": newton_divided_backward},
        {"name": "Ньютон (конечные разности), 1-я формула", "func": newton_finite_forward},
        {"name": "Ньютон (конечные разности), 2-я формула", "func": newton_finite_backward},
        {"name": "Гаусс, 1-я формула", "func": gauss_first},
        {"name": "Гаусс, 2-я формула", "func": gauss_second},
        {"name": "Стирлинг", "func": stirling},
        {"name": "Бессель", "func": bessel},
    ]
