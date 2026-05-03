from methods.base import Method, ResultMethod

class SecantMethod(Method):
    def solve(self, eq, **kwargs) -> ResultMethod:
        a = kwargs.get('a')
        b = kwargs.get('b')
        eps = kwargs.get('eps', 1e-4)

        if eq.f(a) * eq.ddf(a) > 0:
            x0 = a
            x1 = b
        else:
            x0 = b
            x1 = a

        history = []
        for i in range(1, 101):
            f0 = eq.f(x0)
            f1 = eq.f(x1)
            
            if abs(f1 - f0) < 1e-12:
                return ResultMethod(success=False, error_message="Деление на ноль: разность функций близка к 0")
                
            x_next = x1 - f1 * (x1 - x0) / (f1 - f0)
            err = abs(x_next - x1)
            
            history.append([i, x_next, eq.f(x_next), err])
            
            if err < eps:
                return ResultMethod(solutions=[x_next], iterations_data=history, errors=[err])
                
            x0 = x1
            x1 = x_next
            
        return ResultMethod(success=False, error_message="Метод секущих не сошелся за 100 итераций")