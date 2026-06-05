from src.methods.method import Method, BaseIntegrationMethod
import math

from typing import Callable, Any

class RectangleMidMethod(Method, BaseIntegrationMethod):
    def __init__(self, k):
        super().__init__(k)

    def _calculate_integral(self, f: Callable, a: float, b: float, n: int) -> float:
        if a >= b: return 0.0
        h = (b - a) / n
        total = 0.0
        for i in range(n):
            y = f(a + (i + 0.5) * h)
            self._check_value(y)
            total += y
        return total * h
