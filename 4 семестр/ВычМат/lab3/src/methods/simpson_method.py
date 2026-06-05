from src.methods.method import Method, BaseIntegrationMethod
from typing import Callable


class SimpsonMethod(Method, BaseIntegrationMethod):
    def __init__(self, k):
        super().__init__(k)

    def _calculate_integral(self, f: Callable, a: float, b: float, n: int) -> float:
        h = (b - a) / n
        y_a, y_b = f(a), f(b)
        self._check_value(y_a); self._check_value(y_b)
        
        total = y_a + y_b
        for i in range(1, n):
            y = f(a + i * h)
            self._check_value(y)
            if i % 2 == 0:
                total += 2 * y
            else:
                total += 4 * y
        return (h / 3) * total