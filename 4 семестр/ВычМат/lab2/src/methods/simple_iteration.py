# src/methods/simple_iteration.py
from methods.base import Method, ResultMethod

class SimpleIterationMethod(Method):
    def solve(self, eq, x0, eps) -> ResultMethod:
        # Условие 6: проверка сходимости
        if abs(eq.dphi(x0)) >= 1:
            return ResultMethod(success=False, error_message="Условие сходимости |phi'(x)| < 1 не выполнено")
            
        x = x0
        history = []
        for i in range(1, 101):
            x_next = eq.phi(x)
            err = abs(x_next - x)
            history.append([i, x_next, eq.f(x_next), err])
            if err < eps:
                return ResultMethod(solutions=[x_next], iterations_data=history, errors=[err])
            x = x_next
        return ResultMethod(success=False, error_message="Превышено число итераций")