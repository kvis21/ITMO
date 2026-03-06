from src.algorithms.gausian import GausianSeidel
from src.input import input_matrix
from src.utils import greedy_reordering, brute_force_reorderding

import pandas as pd


def main():
    try:
        while True:
            try:
                print("\n"+"#"*80 + "\n")
                matrix, epsilon = input_matrix()

                solver = GausianSeidel(epsilon)

                matrix = greedy_reordering(matrix)

                result = solver.compute(matrix)
                if "error" in result:
                    print(f"Ошибка: {result['error']}")
                else:
                    result = pd.Series(result)
                    result.to_csv("answer.csv", index=True)

                    result["x"] = [val for val in result["x"]]
                    result["errors"] = [val for val in result["errors"]]

                    print("\nВывод результатов:")
                    for key, value in result.items():
                        print(f"{key}: {value}")
            except (FileNotFoundError, ValueError) as e:
                print(e)
                continue
            except KeyboardInterrupt :
                print("Ввод прерван")
                break

            print("\n" + "-" * 40)
            choice = input("Хотите решить еще одну матрицу? (y/n): ").strip().lower()
            if choice != 'y':
                print("Завершение работы.")
                break

    except (TypeError) as e:
        print(e)
        print("Завершение работы.")

if __name__ == "__main__":
    main()
