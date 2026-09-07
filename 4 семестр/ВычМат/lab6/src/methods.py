from typing import Callable, List, Tuple


def euler(f: Callable[[float, float], float],
          x0: float, y0: float, xn: float, h: float) -> Tuple[List[float], List[float]]:
    n = round((xn - x0) / h)
    x = [x0 + i * h for i in range(n + 1)]
    y = [0.0] * (n + 1)
    y[0] = y0
    for i in range(n):
        y[i + 1] = y[i] + h * f(x[i], y[i])
    return x, y


def runge_kutta_4(f: Callable[[float, float], float],
                  x0: float, y0: float, xn: float, h: float) -> Tuple[List[float], List[float]]:
    n = round((xn - x0) / h)
    x = [x0 + i * h for i in range(n + 1)]
    y = [0.0] * (n + 1)
    y[0] = y0
    for i in range(n):
        k1 = h * f(x[i], y[i])
        k2 = h * f(x[i] + h / 2, y[i] + k1 / 2)
        k3 = h * f(x[i] + h / 2, y[i] + k2 / 2)
        k4 = h * f(x[i] + h, y[i] + k3)
        y[i + 1] = y[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return x, y


def milne(f: Callable[[float, float], float],
          x0: float, y0: float, xn: float, h: float) -> Tuple[List[float], List[float]]:
    n = round((xn - x0) / h)
    if n < 4:
        return runge_kutta_4(f, x0, y0, xn, h)

    x_rk, y_rk = runge_kutta_4(f, x0, y0, x0 + 3 * h, h)

    x = [x0 + i * h for i in range(n + 1)]
    y = [0.0] * (n + 1)
    for i in range(4):
        y[i] = y_rk[i]

    for i in range(4, n + 1):
        f_im3 = f(x[i - 3], y[i - 3])
        f_im2 = f(x[i - 2], y[i - 2])
        f_im1 = f(x[i - 1], y[i - 1])

        y_pred = y[i - 4] + (4 * h / 3) * (2 * f_im3 - f_im2 + 2 * f_im1)

        f_pred = f(x[i], y_pred)

        y[i] = y[i - 2] + (h / 3) * (f_im2 + 4 * f_im1 + f_pred)

    return x, y
