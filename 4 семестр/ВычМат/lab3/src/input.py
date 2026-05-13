from src.data import FUNCTIONS, Function
from src.method_manager import MethodManager
from src.methods.method import Method

def get_function() -> Function:
    print("Выберите функцию:")
    for i, f in enumerate(FUNCTIONS):
        print(f"{i + 1}. {f.formula_str}")
        
    while True:
        try:
            choice = int(input("Ваш выбор: "))
            return FUNCTIONS[choice - 1]
        except ValueError:
            print(f"Ошибка ввода: введите целое число от 1 до {len(FUNCTIONS)}!")
            
def get_borders() -> tuple[float, float]:
    while True:
        try:
            a = float(input("Введите начальный предел интегрирования: ").replace(',', '.'))
            b = float(input("Введите конечный предел интегрирования: ").replace(',', '.'))
            if a < b:
                return a, b
            else:
                print("Ошибка ввода: начальный предел интегрирования должен быть меньше конечного предела интегрирования!")
                
        except ValueError:
            print("Ошибка ввода: введите числа")

def get_eps() -> float:
    while True:
        try:
            eps = float(input("Введите точность: ").replace(',', '.'))
            if eps > 0:
                return eps
            else:
                print("Ошибка ввода: точность должна быть положительна!")
        except ValueError:
            print("Ошибка ввода: введите число")
            

def get_method() -> Method:
    print("Выберите метод интегрирования:")
    for i, (method_name, _) in enumerate(MethodManager().get_methods().items()):
        print(f"{i + 1}. {method_name}")
        
    while True:
        try:
            choice = int(input("Ваш выбор: "))
            if 1 <= choice <= len(MethodManager().get_methods()):
                print(f"Выбранный метод: {MethodManager().get_method_name(choice - 1)}")
                return MethodManager().get_method(choice - 1)
        except ValueError:
            print(f"Ошибка ввода: введите целое число от 1 до {len(MethodManager().get_methods())}!")
        except IndexError:
            print(f"Ошибка ввода: введите целое число от 1 до {len(MethodManager().get_methods())}!")
        
        
    