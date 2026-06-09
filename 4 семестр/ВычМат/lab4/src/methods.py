# methods.py
import math
from utils import solve_linear_system
from data import ApproximationResult

def calculate_metrics(phi, y_list, n):
    """Вычисляет S, СКО (delta) и коэффициент детерминации R^2"""
    S = sum((phi[i] - y_list[i]) ** 2 for i in range(n))
    delta = math.sqrt(S / n)
    
    y_mean = sum(y_list) / n
    ss_tot = sum((y - y_mean) ** 2 for y in y_list)
    
    if ss_tot < 1e-12:
        R2 = 1.0 if S < 1e-12 else 0.0
    else:
        R2 = 1.0 - (S / ss_tot)
        
    return S, delta, R2

def calculate_pearson(x_list, y_list, n):
    """Вычисляет коэффициент корреляции Пирсона для линейной зависимости"""
    x_mean = sum(x_list) / n
    y_mean = sum(y_list) / n
    
    num = sum((x_list[i] - x_mean) * (y_list[i] - y_mean) for i in range(n))
    den_x = sum((x - x_mean) ** 2 for x in x_list)
    den_y = sum((y - y_mean) ** 2 for y in y_list)
    
    if den_x * den_y == 0:
        return 0.0
    return num / math.sqrt(den_x * den_y)

def linear_approximation(n, x_list, y_list) -> ApproximationResult:
    try:
        sum_x, sum_y = sum(x_list), sum(y_list)
        sum_xx = sum(x ** 2 for x in x_list)
        sum_xy = sum(x * y for x, y in zip(x_list, y_list))
        a, b = solve_linear_system([[sum_xx, sum_x], [sum_x, n]], [sum_xy, sum_y])
        phi = [a * x + b for x in x_list]
        S, delta, R2 = calculate_metrics(phi, y_list, n)
        r = calculate_pearson(x_list, y_list, n)
        return ApproximationResult("Линейная", [a, b], phi, S, delta, R2, "Успешно", pearson_r=r)
    except Exception as e:
        return ApproximationResult("Линейная", None, None, float('nan'), float('nan'), float('nan'), f"Ошибка: {e}")

def polynomial_2_approximation(n, x_list, y_list) -> ApproximationResult:
    try:
        sum_x = sum(x_list)
        sum_x2 = sum(x ** 2 for x in x_list)
        sum_x3 = sum(x ** 3 for x in x_list)
        sum_x4 = sum(x ** 4 for x in x_list)
        sum_y = sum(y_list)
        sum_xy = sum(x * y for x, y in zip(x_list, y_list))
        sum_x2y = sum((x ** 2) * y for x, y in zip(x_list, y_list))
        
        A = [[sum_x4, sum_x3, sum_x2], [sum_x3, sum_x2, sum_x], [sum_x2, sum_x, n]]
        B = [sum_x2y, sum_xy, sum_y]
        a2, a1, a0 = solve_linear_system(A, B)
        phi = [a2 * (x ** 2) + a1 * x + a0 for x in x_list]
        S, delta, R2 = calculate_metrics(phi, y_list, n)
        return ApproximationResult("Полином 2-й степени", [a2, a1, a0], phi, S, delta, R2, "Успешно")
    except Exception as e:
        return ApproximationResult("Полином 2-й степени", None, None, float('nan'), float('nan'), float('nan'), f"Ошибка: {e}")

def polynomial_3_approximation(n, x_list, y_list) -> ApproximationResult:
    try:
        sum_x = sum(x_list)
        sum_x2 = sum(x ** 2 for x in x_list)
        sum_x3 = sum(x ** 3 for x in x_list)
        sum_x4 = sum(x ** 4 for x in x_list)
        sum_x5 = sum(x ** 5 for x in x_list)
        sum_x6 = sum(x ** 6 for x in x_list)
        sum_y = sum(y_list)
        sum_xy = sum(x * y for x, y in zip(x_list, y_list))
        sum_x2y = sum((x ** 2) * y for x, y in zip(x_list, y_list))
        sum_x3y = sum((x ** 3) * y for x, y in zip(x_list, y_list))

        A = [[sum_x6, sum_x5, sum_x4, sum_x3], [sum_x5, sum_x4, sum_x3, sum_x2], [sum_x4, sum_x3, sum_x2, sum_x], [sum_x3, sum_x2, sum_x, n]]
        B = [sum_x3y, sum_x2y, sum_xy, sum_y]
        a3, a2, a1, a0 = solve_linear_system(A, B)
        phi = [a3 * (x ** 3) + a2 * (x ** 2) + a1 * x + a0 for x in x_list]
        S, delta, R2 = calculate_metrics(phi, y_list, n)
        return ApproximationResult("Полином 3-й степени", [a3, a2, a1, a0], phi, S, delta, R2, "Успешно")
    except Exception as e:
        return ApproximationResult("Полином 3-й степени", None, None, float('nan'), float('nan'), float('nan'), f"Ошибка: {e}")

def exponential_approximation(n, x_list, y_list) -> ApproximationResult:
    name = "Экспоненциальная"
    if any(y <= 0 for y in y_list): 
        return ApproximationResult(name, None, None, float('nan'), float('nan'), float('nan'), "Неприменимо (y ≤ 0)")
    try:
        lin_y = [math.log(y) for y in y_list]
        sum_x, sum_lin_y = sum(x_list), sum(lin_y)
        sum_xx = sum(x ** 2 for x in x_list)
        sum_x_liny = sum(x * ly for x, ly in zip(x_list, lin_y))
        b_lin, a_lin = solve_linear_system([[sum_xx, sum_x], [sum_x, n]], [sum_x_liny, sum_lin_y])
        a, b = math.exp(a_lin), b_lin
        phi = [a * math.exp(b * x) for x in x_list]
        S, delta, R2 = calculate_metrics(phi, y_list, n)
        return ApproximationResult(name, [a, b], phi, S, delta, R2, "Успешно")
    except Exception as e:
        return ApproximationResult(name, None, None, float('nan'), float('nan'), float('nan'), f"Ошибка: {e}")

def logarithmic_approximation(n, x_list, y_list) -> ApproximationResult:
    name = "Логарифмическая"
    if any(x <= 0 for x in x_list): 
        return ApproximationResult(name, None, None, float('nan'), float('nan'), float('nan'), "Неприменимо (x ≤ 0)")
    try:
        lin_x = [math.log(x) for x in x_list]
        sum_lin_x, sum_y = sum(lin_x), sum(y_list)
        sum_lin_xx = sum(lx ** 2 for lx in lin_x)
        sum_lin_x_y = sum(lx * y for lx, y in zip(lin_x, y_list))
        a, b = solve_linear_system([[sum_lin_xx, sum_lin_x], [sum_lin_x, n]], [sum_lin_x_y, sum_y])
        phi = [a * math.log(x) + b for x in x_list]
        S, delta, R2 = calculate_metrics(phi, y_list, n)
        return ApproximationResult(name, [a, b], phi, S, delta, R2, "Успешно")
    except Exception as e:
        return ApproximationResult(name, None, None, float('nan'), float('nan'), float('nan'), f"Ошибка: {e}")

def power_approximation(n, x_list, y_list) -> ApproximationResult:
    name = "Степенная"
    if any(x <= 0 for x in x_list) or any(y <= 0 for y in y_list): 
        return ApproximationResult(name, None, None, float('nan'), float('nan'), float('nan'), "Неприменимо (x или y ≤ 0)")
    try:
        lin_x = [math.log(x) for x in x_list]
        lin_y = [math.log(y) for y in y_list]
        sum_lin_x, sum_lin_y = sum(lin_x), sum(lin_y)
        sum_lin_xx = sum(lx ** 2 for lx in lin_x)
        sum_lin_x_liny = sum(lx * ly for lx, ly in zip(lin_x, lin_y))
        b_lin, a_lin = solve_linear_system([[sum_lin_xx, sum_lin_x], [sum_lin_x, n]], [sum_lin_x_liny, sum_lin_y])
        a, b = math.exp(a_lin), b_lin
        phi = [a * (x ** b) for x in x_list]
        S, delta, R2 = calculate_metrics(phi, y_list, n)
        return ApproximationResult(name, [a, b], phi, S, delta, R2, "Успешно")
    except Exception as e:
        return ApproximationResult(name, None, None, float('nan'), float('nan'), float('nan'), f"Ошибка: {e}")