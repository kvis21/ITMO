import math
from typing import Callable
from src.methods.method import Method, BaseIntegrationMethod
from src.data import Result, Callback

class RectangleLeftMethod(Method, BaseIntegrationMethod):
    def __init__(self, k):
        super().__init__(k)

    def _calculate_integral(self, f: Callable, a: float, b: float, n: int) -> float:
        h = (b - a) / n
        total = 0.0

        for i in range(n):  # От 0 до n-1
            x_i = a + i * h
            y_i = f(x_i)
            self._check_value(y_i)
            total += y_i
            
        return total * h
