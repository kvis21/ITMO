from methods.base import Method, ResultMethod


class ChordMethod(Method):
    def solve(self, eq, **kwargs) -> ResultMethod:
        a = kwargs.get('a')
        b = kwargs.get('b')
        eps = kwargs.get('eps', 1e-4)
        max_iter = kwargs.get('max_iter', 100)

        for i in range(1, max_iter + 1):
            c = (b -a) /2


            if eq.f(c) * eq.f(a) > 0:
                a = c
                err = abs(b - c) 
            else:
                b = c
                err = abs(a - c) 

            if err < eps:
                return c 
            



            