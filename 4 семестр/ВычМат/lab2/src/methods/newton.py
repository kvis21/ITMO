import numpy as np
from methods.base import Method, ResultMethod

class NewtonMethod(Method):
    def solve(self, equation, **kwargs) -> ResultMethod:
        eps = kwargs.get('eps', 1e-4)
        
        # Если это система
        if hasattr(equation, 'jacobian'):
            x = kwargs.get('x0').astype(float)
            history = []
            for i in range(100):
                f_val = equation.evaluate(x)
                j_val = equation.jacobian(x)
                delta = np.linalg.solve(j_val, -f_val)
                x = x + delta
                err = np.linalg.norm(delta)
                history.append(err)
                if err < eps:
                    return ResultMethod(solutions=x.tolist(), iterations_data=history, success=True)
            return ResultMethod(error_message="Метод не сошелся за 100 итераций", success=False)
