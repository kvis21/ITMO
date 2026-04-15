from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, List
from src.equation import SystemEquation


class ResultMethod:
    def __init__(self, solutions: List[float], iterations_data: list[Any], errors: List[float]):
        self.solutions = solutions
        self.iterations_data = iterations_data
        self.errors = errors

    def __init__(self, error: str):
        pass


class Method(ABC):
    @abstractmethod 
    def solve(equation: SystemEquation) -> ResultMethod: pass




class MethodType(Enum):
    CHORD = "Метод хорд"
    SECANT = "Метод секущих"
    SIMPLE_ITERATION = "Метод простых итераций"
    NEWTON = "Метод Ньютона"