# data.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ApproximationResult:
    name: str                            # Название метода
    coefficients: Optional[List[float]]  # Список коэффициентов [a, b, ...]
    phi: Optional[List[float]]           # Вычисленные значения phi(x_i)
    S: float                             # Мера отклонения S
    delta: float                         # Среднеквадратичное отклонение (СКО)
    R2: float                            # Коэффициент детерминации R^2
    status: str                          # Статус ("Успешно" или описание ошибки)
    pearson_r: Optional[float] = None    # Коэффициент корреляции Пирсона (только для линейной)

@dataclass
class SolverState:
    x_data: List[float]
    y_data: List[float]
    n: int
    results: List[ApproximationResult]
    best_result: Optional[ApproximationResult]