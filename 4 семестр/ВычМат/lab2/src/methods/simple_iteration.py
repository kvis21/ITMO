from methods.base import Method, ResultMethod

class SimpleIterationMethod(Method):
    def solve(self, eq, **kwargs) -> ResultMethod:
        x0 = kwargs.get('x0')
        eps = kwargs.get('eps', 0.0001)
        max_iter = kwargs.get('max_iter', 100)
        
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
            
                err = abs(x_next - x)
                
                history.append([i, x_next, eq.f(x_next), err])
                
                if err < eps:
                    return ResultMethod(
                        solutions=[x_next], 
                        iterations_data=history, 
                        errors=[err],
                        success=True 
                    )
                
                x = x_next
                
                if abs(x) > 1e10:
                    return ResultMethod(success=False, error_message="Метод расходится (значения x слишком велики)")
                    
            except Exception as e:
                return ResultMethod(success=False, error_message=f"Ошибка вычислений: {e}")

        return ResultMethod(
            success=False, 
            error_message=f"Превышено максимальное число итераций ({max_iter})"
        )