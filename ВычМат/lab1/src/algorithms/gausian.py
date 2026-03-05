from src.algorithms.base import AlgoBase
from src.structures import Matrix, RowType
from src.utils import norm, get_left_part, get_right_part
from itertools import permutations
from numpy import zeros_like
from pandas import DataFrame
from typing import Tuple, Optional, Dict, Any

#метод гауса-зейделя
class GausianSeidel(AlgoBase): 
    def __init__(self, epsilon = 0.01):
        self.epsilon = epsilon
        self.max_iter = 1000

    def compute(self, mat: Matrix) -> Dict[str, Any]:
        print("Введена матрица:")
        print(DataFrame(mat).to_string(index=False, header=False))

        mat = self._greedy_reordering(mat)
        if mat is None:
            print("Диагональное преобладание недостижимо для данной матрицы.")
            return {"error": "Диагональное преобладание недостижимо для данной матрицы."}
        
        a = get_left_part(mat)
        b = get_right_part(mat)
        c, d = self._get_start_value(a, b)

        matrix_norm = norm(c)

        x = zeros_like(b)
        iteration_count = 0
        while self.max_iter > iteration_count: 
            iteration_count += 1

            x_new = self._iteration(c, d, x.copy())

            error = x_new - x
            if norm(error) < self.epsilon:
                return {
                    "x": x_new,                
                    "iterations": iteration_count,        
                    "errors": error,    
                    "matrix_norm": matrix_norm            
                }
            x = x_new
        

    def _iteration(self, c: Matrix, d: RowType, x: RowType) -> RowType:
        n = len(d)
        for i in range(n):
            s = sum(c[i][j] * x[j] for j in range(n))
            x[i] = d[i] + s
        return x

    def _get_start_value(self, a: Matrix, b: RowType) -> Tuple[Matrix, RowType]:
        d = zeros_like(b)
        c = zeros_like(a)

        for i in range(len(a)):
            for j in range(len(a[0])):
                c[i][j] = -(a[i][j]/a[i][i]) if i != j else 0
            d[i] = b[i]/a[i][i]
        return c, d
    
    def _reorder_to_diagonal_dominance(self, mat: Matrix) -> Optional[Matrix]:
        n = len(mat)
        for p in permutations(range(n)):
            new_mat = mat[list(p)]
            if self._check_dominance(get_left_part(new_mat)):
                return new_mat
        return None
    
    def _greedy_reordering(self, mat: Matrix) -> Optional[Matrix]:
    
        n = len(mat)
        a = get_left_part(mat).copy()
        used_rows = set()
        new_order = []
        
        for col in range(n):
            best_row = -1
            best_val = -1
            for row in range(n):
                if row not in used_rows and abs(a[row][col]) > best_val:
                    best_val = abs(a[row][col])
                    best_row = row
            
            if best_row == -1:
                return None
            
            new_order.append(best_row)
            used_rows.add(best_row)
        
        return [mat[row_index] for row_index in new_order]

    def _check_dominance(self, a: Matrix) -> bool:
        n = len(a)
        has_strict = False
        for i in range(n):
            diag = abs(a[i][i])
            row_sum = sum(abs(a[i][j]) for j in range(n) if i != j)
            if diag < row_sum:
                return False
            if diag > row_sum:
                has_strict = True
        return has_strict
