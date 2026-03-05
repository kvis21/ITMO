from src.structures import Matrix, RowType

import numpy as np

def norm(obj: Matrix | RowType) -> float:
    arr = np.array(obj)
    if arr.ndim == 1: return np.max(np.abs(arr))
    elif arr.ndim == 2: return np.max(np.sum(np.abs(arr), axis=1))

def get_left_part(mat: Matrix) -> Matrix:
    return [row[:-1] for row in mat]

def get_right_part(mat: Matrix) -> RowType:
    return [row[-1] for row in mat]

def generate_matrix(n: int) -> Matrix:
    
    pass