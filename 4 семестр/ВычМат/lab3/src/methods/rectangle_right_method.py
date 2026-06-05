from src.methods.method import Method, BaseIntegrationMethod
from typing import Callable, Any


class RectangleRightMethod(Method, BaseIntegrationMethod):
    def __init__(self, k):
        super().__init__(k)

    def _calculate_integral(self, f: Callable, a: float, b: float, n: int) -> float:
        h = (b - a) / n
        
        total = 0.0
        for i in range(1, n + 1):
            y = f(a + i * h)
            self._check_value(y)
            total += y
        return total * h

