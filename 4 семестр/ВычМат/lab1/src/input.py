from src.structures import Matrix, RowType
from src.utils import generate_matrix

from typing import List, Optional, Tuple
import os

def input_matrix() -> Tuple[Matrix, float]:


    while True:
        print("1 - Ввод из файла")
        print("2 - Ввод из консоли")
        print("3 - генерация рандомной матрицы")
        try:
            choice = input().strip()
            if choice == '1':
                return _input_from_file()
            elif choice == '2':
                return _input_from_console()
            elif choice == '3':
                return _input_from_random()
            else:
                print("Ошибка: введите число от 1 до 3")
        except (FileNotFoundError, ValueError) as e:
            print(f"Ошибка: {e}")
            continue
        except Exception as e:
            break

def _input_from_file() -> Tuple[Matrix, float]:
    while True:
        filepath = input("Введите путь к файлу: ").strip()

        if filepath == "": filepath = "data/mat5"

        if not os.path.exists(filepath):
            print(f"Файл '{filepath}' не найден. Попробуйте снова.")
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f]
        
        first_line = lines[0].split()
        n, epsilon = int(first_line[0]), float(first_line[1])
        if len(lines) - 1 < n:
            raise ValueError(f"Ожидалось {n} строк данных, найдено {len(lines) - 1}")
        
        matrix_data = []
        for i in range(1, n + 1):
            row = _parse_row(lines[i], expected_length=n)
            matrix_data.append(row)

        return matrix_data, epsilon

def _input_from_console() -> Tuple[Matrix, float]:
    while True:
        try:
            n, epsilon  = input("Введите размерность матрицы и точность: ").strip().split()[:2]
            n = int(n)
            epsilon = float(epsilon.replace(',', '.'))
            print(f"Размерность = {n}; точность = {epsilon}")
        except ValueError:
            print("Ошибка: введите корректные числовые значения.")
            continue

        matrix_data = []

        if n <= 0:
            print("Размерность должна быть больше 0.")
            continue
        if epsilon <= 0:
            print("Точность должна быть положительным числом.")
            continue

        print(f"введите {n} строк:")
        print("Числа разделяйте пробелами")

        for i in range(n):
            while True:
                line = input(f"Строка {i + 1}: ").strip()
                
                if not line:
                    print("Строка не может быть пустой. Повторите ввод.")
                    continue
                
                row = _parse_row(line, expected_length=n)
                matrix_data.append(row)
                break
        return matrix_data, epsilon

def _input_from_random() -> Tuple[Matrix, float]:
    while True:
        try:
            n, epsilon  = input("Введите размерность матрицы и точность: ").strip().split()[:2]
            if not n or not epsilon: continue
            
            n = int(n)
            epsilon = float(epsilon.replace(',', '.'))
            print(f"Размерность = {n}; точность = {epsilon}")
        except ValueError:
            print("Ошибка: введите корректные числовые значения.")
            continue
        
        if n <= 0:
            print("Размерность должна быть больше 0.")
            continue
        if epsilon <= 0:
            print("Точность должна быть положительным числом.")
            continue

        matrix = generate_matrix(n)
        print(f"Сгенерирована матрица размерности {n}x{n} с точностью {epsilon}")
        return matrix, epsilon
        

def _parse_row(line: str, expected_length: Optional[int] = None) -> List[float]:
    line = line.replace(',', ' ').replace('\t', ' ')
    parts = line.split()
    
    numbers = []
    for part in parts:
        try:
            num = float(part)
            numbers.append(num)
        except ValueError: 
            raise ValueError(f"Невозможно преобразовать '{part}' в число")
    
    if expected_length is not None and len(numbers) != expected_length+1:
        raise ValueError(f"Строка содержит {len(numbers)} чисел, ожидалось {expected_length+1}")
    
    return numbers