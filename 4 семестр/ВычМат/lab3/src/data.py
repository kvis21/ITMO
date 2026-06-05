from dataclasses import dataclass
from typing import Callable, List
from math import sqrt, exp, log, sin


@dataclass
class Result:
    value: float
    number_split: int

@dataclass
class Callback:
    error: str = None
    result: Result = None

@dataclass
class Function:
    formula_str: str
    function: Callable
    # Точки, где функция может иметь разрыв (например, 0 для 1/x)
    singular_points: List[float] 
    # Порядок p для оценки сходимости в этих точках (p=1 для 1/x, p=0.5 для 1/sqrt(x))
    p_orders: List[float] 

FUNCTIONS = [
    Function("x^2 + 2x + 1", lambda x: x**2 + 2*x + 1, [], []),
    Function("e^x", exp, [], []),
    Function("ln(x)", log, [0.0], [0.99]), 
    Function("1/sqrt(x)", lambda x: 1/sqrt(x) if x > 0 else float('inf'), [0.0], [0.5]),
    Function("1/x", lambda x: 1/x if x != 0 else float('inf'), [0.0], [1.0]),
]