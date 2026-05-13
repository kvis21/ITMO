from src.methods.method import Method, BaseIntegrationMethod
from src.data import Callback, Result

from typing import Callable, Any


class SimpsonMethod(Method, BaseIntegrationMethod):
    def _calculate_integral(self, f: Callable, a: float, b: float, n: int) -> float:
        # n должно быть четным для метода Симпсона
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

    def solve(self, **kwargs) -> Callback:
        f, a, b, eps = self._get_params(kwargs)
        n, iterations = 4, 0 # Начинаем с четного n
        try:
            i_prev = self._calculate_integral(f, a, b, n)
            while iterations < 20:
                n *= 2
                i_curr = self._calculate_integral(f, a, b, n)
                # Для Симпсона порядок точности k=4, делитель 2^4 - 1 = 15
                if abs(i_curr - i_prev) / 15 <= eps:
                    return Callback(result=Result(i_curr, n))
                i_prev, iterations = i_curr, iterations + 1
            return Callback(result=Result(i_curr, n))
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            return Callback(error=f"Интеграл не существует: функция имеет разрыв.")
        except Exception as e:
            return Callback(error=f"Критическая ошибка при вычислении: {str(e)}")