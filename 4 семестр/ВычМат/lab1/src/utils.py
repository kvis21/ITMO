from src.structures import Matrix, RowType

from typing import Optional
from itertools import permutations
import random

def matrix_norm(mat: Matrix) -> float:
    return max(sum(abs(element) for element in row) for row in mat)

def vector_norm(vec: RowType) -> float:
    return max(abs(x) for x in vec)

def get_left_part(mat: Matrix) -> Matrix:
    return [row[:-1] for row in mat]

def get_right_part(mat: Matrix) -> RowType:
    return [row[-1] for row in mat]

def generate_matrix(n: int) -> Matrix:

    matrix = []
    for i in range(n):
        row = []
        row_sum = 0

        for j in range(n):
            if i == j:
                row.append(0) 
            else:
                val = random.uniform(-10, 10)
                row.append(val)
                row_sum += abs(val)
        
        matrix_diag_val = row_sum + random.uniform(1, 10)
      
        if random.random() > 0.5:
            matrix_diag_val *= -1
        row[i] = matrix_diag_val
        
        b_val = random.uniform(-10, 10)
        row.append(b_val)
        
        matrix.append(row)
        
    return matrix

def brute_force_reorderding(mat: Matrix) -> Optional[Matrix]:
    n = len(mat)
    for p in permutations(range(n)):
        new_mat = mat[list(p)]
        if check_dominance(get_left_part(new_mat)):
            return new_mat
    return None

def greedy_reordering(mat: Matrix) -> Optional[Matrix]:

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

def check_dominance(a: Matrix) -> bool:
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