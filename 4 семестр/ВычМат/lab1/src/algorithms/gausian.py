from src.algorithms.base import AlgoBase
from src.structures import Matrix, RowType
from src.utils import get_left_part, get_right_part, matrix_norm, vector_norm

from numpy import zeros_like
from pandas import DataFrame
from typing import Tuple, Optional, Dict, Any

#метод гауса-зейделя
class GausianSeidel(AlgoBase): 
    def __init__(self, epsilon = 0.01):
        self.epsilon = epsilon
        self.max_iter = 1000

    def compute(self, mat: Optional[Matrix]) -> Dict[str, Any]:
        print("Введена матрица:")
        print(DataFrame(mat).to_string(index=False, header=False))

        if mat is None:
            print("Диагональное преобладание недостижимо для данной матрицы.")
            return {"error": "Диагональное преобладание недостижимо для данной матрицы."}
        
        a = get_left_part(mat)
        b = get_right_part(mat)
        c, d = self._get_start_value(a, b)

        mat_norm = matrix_norm(c)

        if mat_norm >= 1:
            print("норма матрицы > 1. матрица может не сходится.")

        x = zeros_like(b).tolist()
        iteration_count = 0
        while self.max_iter > iteration_count: 
            iteration_count += 1

            x_new = self._iteration(c, d, x.copy())

            error = [x_new[i] - x[i] for i in range(len(x))]
            if vector_norm(error) < self.epsilon:
                return {
                    "x": x_new,                
                    "iterations": iteration_count,        
                    "errors": error,    
                    "matrix_norm": mat_norm            
                }
            x = x_new
        else:
            return {"error": "Достигнут лимит итераций"}
        

    def _iteration(self, c: Matrix, d: RowType, x: RowType) -> RowType:
        n = len(d)
        for i in range(n):
            s = sum(c[i][j] * x[j] for j in range(n))
            x[i] = d[i] + s
        return x

    def _get_start_value(self, a: Matrix, b: RowType) -> Tuple[Matrix, RowType]:
        d = zeros_like(b).tolist()
        c = zeros_like(a).tolist()

        for i in range(len(a)):
            for j in range(len(a[0])):
                c[i][j] = -(a[i][j]/a[i][i]) if i != j else 0
            d[i] = b[i]/a[i][i]
        return c, d
    