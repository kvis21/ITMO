from src.input import *
from src.methods.method import Method
from src.data import Function, Callback

if __name__ == '__main__':
    try:
        while True:
            function: Function = get_function()
            a, b = get_borders()
            method: Method = get_method()
            eps: float = get_eps()
            
            callback: Callback = method.solve(
                function = function.function, 
                a=a, 
                b=b, 
                eps=eps
            )
            
            if callback.result is not None:
                print(f"Значение интеграла: {callback.result.value}")
                print(f"Количество разбиений интервала интегрирования для достижения требуемой точности: {callback.result.number_split}")
            else:
                print(f"{callback.error}")
    except KeyboardInterrupt:
        print("\nЗавершение программы")