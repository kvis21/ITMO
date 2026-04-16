from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, List, Optional
from dataclasses import dataclass

@dataclass
class ResultMethod:
    solutions: Optional[List[float]] = None
    iterations_data: Optional[List[Any]] = None
    errors: Optional[List[float]] = None
    error_message: Optional[str] = None
    success: bool = True

class Method(ABC):
    @abstractmethod 
    def solve(self, equation: Any, **kwargs) -> ResultMethod:
        """Метод решения, принимающий объект уравнения/системы и параметры (a, b, eps, x0)"""
        pass

class MethodType(Enum):
    CHORD = "Метод хорд"
    SECANT = "Метод секущих"
    SIMPLE_ITERATION = "Метод простых итераций"
    NEWTON = "Метод Ньютона"