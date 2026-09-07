from typing import Callable, List, Optional

from methods import euler, runge_kutta_4


def runge_rule(f: Callable[[float, float], float],
               x0: float, y0: float, xn: float, h: float,
               order: int,
               method: Callable = runge_kutta_4) -> float:
    x_h, y_h = method(f, x0, y0, xn, h)
    x_h2, y_h2 = method(f, x0, y0, xn, h / 2)

    r = abs(y_h[-1] - y_h2[-1]) / (2 ** order - 1)
    return r


def exact_max_error(y_approx: List[float], y_exact: List[Optional[float]]) -> Optional[float]:
    vals = [abs(a - e) for a, e in zip(y_approx, y_exact) if e is not None]
    return max(vals) if vals else None
