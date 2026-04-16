from methods.base import Method, ResultMethod

class ChordMethod(Method):
    def solve(self, eq, **kwargs) -> ResultMethod:
        a = kwargs.get('a')
        b = kwargs.get('b')
        eps = kwargs.get('eps', 1e-4)

        # Условие 5: Выбор неподвижного конца (c) и начального приближения (x)
        if eq.f(a) * eq.ddf(a) > 0:
            c = a  # Неподвижный конец
            x = b  # Подвижный конец (начальное приближение x0)
        else:
            c = b
            x = a

        history = []
        for i in range(1, 101):
            fx = eq.f(x)
            fc = eq.f(c)
            
            # Защита от деления на ноль
            if abs(fx - fc) < 1e-12:
                return ResultMethod(success=False, error_message="Деление на ноль: f(x) равно f(c)")

            # Шаг метода хорд
            x_next = x - fx * (x - c) / (fx - fc)
            err = abs(x_next - x)
            
            history.append([i, x_next, eq.f(x_next), err])
            
            if err < eps:
                return ResultMethod(solutions=[x_next], iterations_data=history, errors=[err])
            
            x = x_next
            
        return ResultMethod(success=False, error_message="Метод хорд не сошелся за 100 итераций")