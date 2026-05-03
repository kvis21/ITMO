from methods.base import Method, ResultMethod

class ChordMethod(Method):
    def solve(self, eq, **kwargs) -> ResultMethod:
        a = kwargs.get('a')
        b = kwargs.get('b')
        eps = kwargs.get('eps', 1e-4)
        max_iter = kwargs.get('max_iter', 100)
        
        if eq.f(a) * eq.ddf(a) > 0:
            c = a  
            x = b  
        else:
            c = b
            x = a

        history = []
        for i in range(1, max_iter+1):
            fx = eq.f(x)
            fc = eq.f(c)
            
            x_next = x - fx * (x - c) / (fx - fc)
            err = abs(x_next - x)
            
            history.append([i, x_next, eq.f(x_next), err])
            
            if err < eps:
                return ResultMethod(solutions=[x_next], iterations_data=history, errors=[err])
            
            x = x_next
            
        return ResultMethod(success=False, error_message=f"Метод хорд не сошелся за {max_iter} итераций")