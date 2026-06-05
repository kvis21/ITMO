from src.methods.method import Method, BaseIntegrationMethod

from typing import Callable, Any


class TrapezoidMethod(Method, BaseIntegrationMethod):
    def __init__(self, k):
        super().__init__(k)

    def _calculate_integral(self, f: Callable, a: float, b: float, n: int) -> float:
        h = (b - a) / n
        y_start, y_end = f(a), f(b)
        self._check_value(y_start); self._check_value(y_end)
        total = (y_start + y_end) / 2
        for i in range(1, n):
            y = f(a + i * h)
            self._check_value(y)
            total += y
        return total * h
