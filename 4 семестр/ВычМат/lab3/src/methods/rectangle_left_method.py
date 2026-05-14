import math
from typing import Callable
from src.methods.method import Method, BaseIntegrationMethod
from src.data import Result, Callback

class RectangleLeftMethod(Method, BaseIntegrationMethod):
    def _calculate_integral(self, f: Callable, a: float, b: float, n: int) -> float:
        h = (b - a) / n
        total = 0.0

        self._check_value(f(a)); self._check_value(f(b))
        
        for i in range(n):  # От 0 до n-1
            x_i = a + i * h
            y_i = f(x_i)
            self._check_value(y_i)
            total += y_i
            
        return total * h

    def solve(self, **kwargs) -> Callback:
        f, a, b, eps = self._get_params(kwargs)

        if any(v is None for v in [f, a, b, eps]):
            return Callback(error="Переданы не все необходимые аргументы (function, a, b, eps).")

        try:
            n = 4
            i_prev = self._calculate_integral(f, a, b, n)
            
            max_iterations = 20 
            
            for _ in range(max_iterations):
                n *= 2
                i_curr = self._calculate_integral(f, a, b, n)
                
                if math.isinf(i_curr):
                    return Callback(error="Интеграл не существует: функция имеет разрыв.")

                if abs(i_curr - i_prev)  <= eps:
                    return Callback(result=Result(value=i_curr, number_split=n))
                    
                i_prev = i_curr

            print("Предупреждение: Интеграл не сошелся к требуемой точности за 20 итераций.")
            print("Предупреждение: Возможно интеграл расходится")
            return Callback(result=Result(i_curr, n))

        except (ValueError, ZeroDivisionError, OverflowError) as e:
            return Callback(error=f"Интеграл не существует: функция имеет разрыв.")
        except Exception as e:
            return Callback(error=f"Критическая ошибка при вычислении: {str(e)}")