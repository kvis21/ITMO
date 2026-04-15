from dataclasses import dataclass
from enum import Enum
from typing import List

class EquationType(Enum):
    SINGLE = "Нелинейное уравнение"
    SYSTEM = "Система нелинейных уравнений"

@dataclass
class SystemEquation:
    func_str: str
    func: callable

    def __str__(self) -> str:
        return self.func_str



