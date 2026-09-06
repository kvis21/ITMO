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
    
    return min(range(len(x_list)), key=lambda i: abs(x_list[i] - x))

def _left_index(x: float, x_list: List[float]) -> int:
    
    idx = 0
    for i in range(len(x_list)):
        if x_list[i] <= x:
            idx = i
    return idx

def _right_index(x: float, x_list: List[float]) -> int:
    
    for i in range(len(x_list)):
        if x_list[i] >= x:
            return i
    return len(x_list) - 1

# ---------------------------------------------------------------------------
# Многочлен Лагранжа
# ---------------------------------------------------------------------------

def lagrange_interpolation(x: float, x_list: List[float], y_list: List[float]) -> InterpolationResult:
    
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
def gauss_first(x: float, x_list: List[float], y_list: List[float]) -> InterpolationResult:
    
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
        value = y_list[c]
        i = c
        if 0 <= i < n - 1:
            value += t * table[1][i]
        max_m = min(c, (n - 1) // 2, n - 1 - c)
        for m in range(1, max_m + 1):
            k_even = 2 * m
            k_odd = 2 * m + 1
            i = c - m
            if 0 <= i < n - k_even:
                factor = 1.0
                for r in range(-(m - 1), m + 1):
                    factor *= (t - r)
                value += table[k_even][i] * factor / math.factorial(k_even)
            if 0 <= i < n - k_odd:
                factor = 1.0
                for r in range(-m, m + 1):
                    factor *= (t - r)
                value += table[k_odd][i] * factor / math.factorial(k_odd)
        return InterpolationResult(name, x, value, "Успешно",
                                   formula=f"Центральный узел x[{c}] = {x_list[c]}, t = {t:.4f}")
    except Exception as e:
        return InterpolationResult(name, x, None, f"Ошибка: {e}")

def gauss_second(x: float, x_list: List[float], y_list: List[float]) -> InterpolationResult:
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
        value = y_list[c]
        i = c - 1
        if 0 <= i < n - 1:
            value += t * table[1][i]
        max_m = min(c, (n - 1) // 2, n - 1 - c)
        for m in range(1, max_m + 1):
            k_even = 2 * m
            k_odd = 2 * m + 1
            i_odd = c - m - 1
            i = c - m
            if 0 <= i < n - k_even:
                factor = 1.0
                for r in range(-m, m):
                    factor *= (t - r)
                value += table[k_even][i] * factor / math.factorial(k_even)
            if 0 <= i_odd < n - k_odd:
                factor = 1.0
                for r in range(-m, m + 1):
                    factor *= (t - r)
                value += table[k_odd][i_odd] * factor / math.factorial(k_odd)
        return InterpolationResult(name, x, value, "Успешно",
                                   formula=f"Центральный узел x[{c}] = {x_list[c]}, t = {t:.4f}")
    except Exception as e:
        return InterpolationResult(name, x, None, f"Ошибка: {e}")

def gauss(x: float, x_list: List[float], y_list: List[float]) -> InterpolationResult:
    name = "Гаусс"
    try:
        mid = (x_list[0] + x_list[-1]) / 2.0
        if x <= mid:
            return gauss_first(x, x_list, y_list)
        return gauss_second(x, x_list, y_list)
    except Exception as e:
        return InterpolationResult(name, x, None, f"Ошибка: {e}")

def stirling(x: float, x_list: List[float], y_list: List[float]) -> InterpolationResult:
    
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
        if 0 <= c - 1  and c < n - 1:
            value += t * (table[1][c - 1] + table[1][c]) / 2.0
        if 0 <= c - 1 < n - 2:
            value += t * t / 2.0 * table[2][c - 1]
        max_m = min(c - 1, n - 2 - c)
        for m in range(1, max_m + 1):
            k_odd = 2 * m + 1
            k_even = 2 * m + 2
            prod = 1.0
            for r in range(1, m + 1):
                prod *= (t * t - r * r)
            factor = t * prod / math.factorial(k_odd)
            value += factor * (table[k_odd][c - m - 1] + table[k_odd][c - m]) / 2.0
            value += table[k_even][c - m - 1] * t * t * prod / math.factorial(k_even)
        return InterpolationResult(name, x, value, "Успешно",
                                   formula=f"Центральный узел x[{c}] = {x_list[c]}, t = {t:.4f}")
    except Exception as e:
        return InterpolationResult(name, x, None, f"Ошибка: {e}")

def bessel(x: float, x_list: List[float], y_list: List[float]) -> InterpolationResult:
    
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
        if 0 <= c < n - 1:
            value += (t - 0.5) * table[1][c]
        max_m = min(c, n - 2 - c)
        for m in range(1, max_m + 1):
            k_even = 2 * m
            k_odd = 2 * m + 1
            prod = 1.0
            for r in range(1, m):
                prod *= (t + r) * (t - r - 1)
            factor = t * (t - 1) * prod / math.factorial(k_even)
            value += factor * (table[k_even][c - m] + table[k_even][c - m + 1]) / 2.0
            factor = (t - 0.5) * t * (t - 1) * prod / math.factorial(k_odd)
            value += table[k_odd][c - m] * factor
        return InterpolationResult(name, x, value, "Успешно",
                                   formula=f"Узел x[{c}] = {x_list[c]}, t = {t:.4f}")
    except Exception as e:
        return InterpolationResult(name, x, None, f"Ошибка: {e}")

def all_methods() -> List[dict]:
    
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
