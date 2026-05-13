from dataclasses import dataclass
from typing import Callable
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
    
    
FUNCTIONS = [
    Function("x^2 + 2x + 1", lambda x: x**2 + 2*x + 1),
    Function("x^3 + 2x^2 + 1", lambda x: x**3 + 2*x**2 + 1),
    Function("x^4 + 2x^3 + 1", lambda x: x**4 + 2*x**3 + 1),
    Function("e^x", exp),
    Function("ln(x)", log),
    Function("1/sqrt(x)", lambda x: 1/sqrt(x)),
    Function("sin(x)", sin),
    Function("1/x", lambda x: 1/x)
]