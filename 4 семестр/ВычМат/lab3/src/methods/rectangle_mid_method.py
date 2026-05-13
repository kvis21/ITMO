from src.methods.method import Method, BaseIntegrationMethod
from src.data import Callback, Result

from typing import Callable, Any

class RectangleMidMethod(Method, BaseIntegrationMethod):
    def _calculate_integral(self, f: Callable, a: float, b: float, n: int) -> float:
        h = (b - a) / n
        total = 0.0
        for i in range(n):
            y = f(a + (i + 0.5) * h)
            self._check_value(y)
            total += y
        return total * h

    def solve(self, **kwargs) -> Callback:
        f, a, b, eps = self._get_params(kwargs)
        n, iterations, max_iter = 4, 0, 20
        try:
            i_prev = self._calculate_integral(f, a, b, n)
            while iterations < max_iter:
                n *= 2
                i_curr = self._calculate_integral(f, a, b, n)
                if abs(i_curr - i_prev) / 3 <= eps: # k=2
                    return Callback(result=Result(i_curr, n))
                i_prev, iterations = i_curr, iterations + 1
            return Callback(result=Result(i_curr, n))
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            return Callback(error=f"Интеграл не существует: функция имеет разрыв.")
        except Exception as e:
            return Callback(error=f"Критическая ошибка при вычислении: {str(e)}")