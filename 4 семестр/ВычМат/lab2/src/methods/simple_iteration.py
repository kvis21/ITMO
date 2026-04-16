from methods.base import Method, ResultMethod

class SimpleIterationMethod(Method):
    def solve(self, eq, **kwargs) -> ResultMethod:
        # Извлекаем параметры из kwargs
        x0 = kwargs.get('x0')
        eps = kwargs.get('eps', 0.0001)
        max_iter = kwargs.get('max_iter', 100)
        
        # Условие 6: проверка сходимости в начальной точке
        try:
            q = abs(eq.dphi(x0))
            if q >= 1:
                return ResultMethod(
                    success=False, 
                    error_message=f"Условие сходимости |phi'(x)| < 1 не выполнено (q={q:.4f}). Попробуйте другое начальное приближение."
                )
        except Exception as e:
            return ResultMethod(success=False, error_message=f"Ошибка при вычислении производной phi: {e}")

        x = float(x0)
        history = []
        
        for i in range(1, max_iter + 1):
            try:
                x_next = eq.phi(x)
                # Для метода простой итерации погрешность часто оценивают через |x_n - x_{n-1}|
                # При q > 0.5 иногда используют формулу с коэффициентом q/(1-q), 
                # но для лабы обычно достаточно abs(x_next - x)
                err = abs(x_next - x)
                
                # Записываем итерацию: [№, x_n, f(x_n), погрешность]
                history.append([i, x_next, eq.f(x_next), err])
                
                if err < eps:
                    return ResultMethod(
                        solutions=[x_next], 
                        iterations_data=history, 
                        errors=[err],
                        success=True # Обязательно добавляем
                    )
                
                x = x_next
                
                # Защита от "разлета" метода
                if abs(x) > 1e10:
                    return ResultMethod(success=False, error_message="Метод расходится (значения x слишком велики)")
                    
            except Exception as e:
                return ResultMethod(success=False, error_message=f"Ошибка вычислений: {e}")

        return ResultMethod(
            success=False, 
            error_message=f"Превышено максимальное число итераций ({max_iter})"
        )