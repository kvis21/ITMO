from dataclasses import dataclass

from src.equation import SystemEquation, EquationType
from src.methods.base import MethodType

def get_task_type() -> EquationType:
    print("выберите тип задачи:")
    print("1: Нелинейное уравнение")
    print("2: Система нелинейных уравнений")
    print("3: Выход")

    mapping = {
        1: EquationType.SINGLE,
        2: EquationType.SYSTEM
    }

    while True:
        task_type: str = input()
        try:
            task_type = int(task_type)
            if task_type in [1, 2, 3]:
                return mapping[task_type]
        except ValueError: pass
        print("введите число от 1 до 3")

def get_method_type(eq_type: EquationType) -> MethodType:
    print(f"Выберите метод, которым хотите решить {eq_type.value.lower()}")
    if eq_type == EquationType.SINGLE:
        print("1: Метод Хорд")
        print("2: Метод Секущих")
        print("3: Метод простых итераций")
    if eq_type == EquationType.SYSTEM:
        print("1. Метод Ньютона")

@dataclass
class InputData:
    equation: SystemEquation


def start_input() -> None: 
    pass
