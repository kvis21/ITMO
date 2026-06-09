def solve_linear_system(A, B):
    """
    Решает СЛАУ Ax = B методом Гаусса с выбором главного элемента.
    A: двумерный список (матрица n x n)
    B: список (вектор свободных членов длины n)
    Returns: список (вектор решений x)
    """
    n = len(A)
    # Создаем расширенную матрицу
    matrix = [A[i] + [B[i]] for i in range(n)]

    for i in range(n):
        max_row = i
        for r in range(i + 1, n):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        if abs(matrix[i][i]) < 1e-12:
            raise ValueError("Матрица СЛАУ вырождена или близка к вырожденной. Решение невозможно.")

        for r in range(i + 1, n):
            factor = matrix[r][i] / matrix[i][i]
            for c in range(i, n + 1):
                matrix[r][c] -= factor * matrix[i][c]

    x = [0] * n
    for i in range(n - 1, -1, -1):
        sum_ax = sum(matrix[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (matrix[i][n] - sum_ax) / matrix[i][i]
        
    return x