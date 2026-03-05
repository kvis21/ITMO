from src.algorithms.gausian import GausianSeidel
from src.input import input_matrix

import pandas as pd

def main():
    matrix, epsilon = input_matrix()

    solver = GausianSeidel(epsilon)
    
    result = solver.compute(matrix)
    result = pd.Series(result)
    result.to_csv("answer.csv", index=True)

    result["x"] = list(map(lambda x: round(x, 8), result["x"]))
    result["errors"] = list(map(lambda x: round(x, 8), result["errors"]))

    print("Вывод:")
    print(result)
    

if __name__ == "__main__":
    main()
