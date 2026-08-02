# data.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class InterpolationResult:
    name: str                        # Название метода
    x: float                         # Точка интерполяции
    value: Optional[float]           # Приближенное значение функции y(x)
    status: str                      # Статус ("Успешно" или описание ошибки)
    formula: Optional[str] = None    # Пояснение: какая формула применена

@dataclass
class SolverState:
    x_data: List[float]
    y_data: List[float]
    n: int
    x: float
    results: List[InterpolationResult]
