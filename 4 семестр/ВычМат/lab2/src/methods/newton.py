from methods.base import Method, ResultMethod
from equation import NonLinearSystem

class NewtonMethod(Method):
    def solve(self, system: NonLinearSystem, **kwargs) -> ResultMethod:
        x0 = kwargs.get('x0')
        eps = kwargs.get('eps', 1e-4)
        max_iter = kwargs.get('max_iter', 100) 
        
        x, y = x0[0], x0[1]
        history = []
        
        for i in range(1, max_iter + 1):
            f_vals = system.evaluate([x, y])
            jac = system.jacobian([x, y])
            
            a, b = jac[0][0], jac[0][1]
            c, d = jac[1][0], jac[1][1]
            
            det = a * d - b * c
            if abs(det) < 1e-12:
                return ResultMethod(success=False, error_message="Определитель Якобиана близок к нулю")
            
            dx = (-f_vals[0] * d - (-f_vals[1] * b)) / det
            dy = (a * (-f_vals[1]) - (c * (-f_vals[0]))) / det
            
            x += dx
            y += dy
            err = max(abs(dx), abs(dy))
            
            history.append([i, x, y, err])
            
            if err < eps:
                return ResultMethod(
                    solutions=[x, y], 
                    iterations_data=history, 
                    errors=[abs(dx), abs(dy)],
                    success=True
                )
                
        return ResultMethod(
            success=False, 
            error_message=f"Метод не сошелся за {max_iter} итераций"
        )