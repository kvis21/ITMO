from src.methods.rectangle_mid_method import RectangleMidMethod
from src.methods.rectangle_right_method import RectangleRightMethod
from src.methods.rectangle_left_method import RectangleLeftMethod
from src.methods.trapezoid_method import TrapezoidMethod
from src.methods.simpson_method import SimpsonMethod
from src.methods.method import Method

from typing import Dict

class MethodManager:
    def __init__(self):
        self.methods = {
            "Метод левых прямоугольников": RectangleLeftMethod(),
            "Метод правых прямоугольников": RectangleRightMethod(),
            "Метод средних прямоугольников": RectangleMidMethod(),
            "Метод трапеций": TrapezoidMethod(),
            "Метод Симпсона": SimpsonMethod()
        }
    
    def __len__(self):
        return len(self.methods)
    
    def get_methods(self) -> Dict[str, Method]:
        return self.methods
    
    def get_method(self, number: int) -> Method:
        if 0<=number<=len(self.methods)-1:
            return list(self.methods.values())[number]
        raise IndexError("Неверный номер метода")
    
    def get_method_name(self, number: int) -> str:
        if 0<=number<=len(self.methods)-1:
            return list(self.methods.keys())[number]
        raise IndexError("Неверный номер метода")
        
        
    
    