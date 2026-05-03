from dataclasses import dataclass
from typing import List, Callable
from math import sin, cos, tan, exp

@dataclass
class NonLinearEquation:
    func_str: str
    f: Callable[[float], float]
    df: Callable[[float], float]     # Первая производная
    ddf: Callable[[float], float]    # Вторая производная
    phi: Callable[[float], float]    # x = phi(x) для итераций
    dphi: Callable[[float], float]   # Производная phi для проверки сходимости

    def __str__(self) -> str:
        return self.func_str

@dataclass
class NonLinearSystem:
    func_str: str
    funcs: List[Callable[[List[float]], float]]
    jacobian: Callable[[List[float]], List[List[float]]]

    def evaluate(self, v: List[float]) -> List[float]:
        """Возвращает вектор значений функций системы для заданного приближения"""
        return [f(v) for f in self.funcs]

    def __str__(self) -> str:
        return self.func_str

EQUATIONS = [
    NonLinearEquation(
        "x^3 - x + 4 = 0",
        lambda x: x**3 - x + 4,
        lambda x: 3*x**2 - 1, # производная 1
        lambda x: 6*x, # производная 2
        lambda x: (x - 4)**(1/3) if x >= 4 else -abs(x-4)**(1/3), # phi
        lambda x: (1/3) * abs(x-4)**(-2/3) # проиводная phi
    ),
    
    NonLinearEquation(
        "x^3 - 3x^2 + 3 = 0",
        lambda x: x**3 - 3*x**2 + 3,
        lambda x: 3*x**2 - 6*x,
        lambda x: 6*x - 6,
        lambda x: (3*x**2 - 3)**(1/3) if (3*x**2 - 3) >= 0 else -abs(3*x**2 - 3)**(1/3),
        lambda x: (1/3) * abs(3*x**2 - 3)**(-2/3) * 6*x
    ),
    NonLinearEquation(
        "x^2",
        lambda x: x**2,
        lambda x: 2*x,
        lambda x: 2,
        lambda x: x,
        lambda x: 1
    ),

    NonLinearEquation(
        "e^x - 5x + 2 = 0",
        lambda x: exp(x) - 5*x + 2,
        lambda x: exp(x) - 5,
        lambda x: exp(x),
        lambda x: (exp(x) + 2) / 5,  # Хорошо сходится для корня ~0.7
        lambda x: exp(x) / 5
    ),
    NonLinearEquation(
        "x^3 - x + 4 = 0",
        lambda x: x**3 - x + 4,
        lambda x: 3*x**2 - 1,
        lambda x: 6*x,
        lambda x: (x - 4)**(1/3) if x >= 4 else -abs(x-4)**(1/3), # пример phi
        lambda x: (1/3) * abs(x-4)**(-2/3)
    )
]

SYSTEMS = [
    NonLinearSystem(
        "sin(x+y)-1.2x=0.1, x^2+y^2=1",
        [
            lambda v: sin(v[0] + v[1]) - 1.2*v[0] - 0.1,
            lambda v: v[0]**2 + v[1]**2 - 1
        ],
        lambda v: [
            [cos(v[0] + v[1]) - 1.2, cos(v[0] + v[1])],
            [2*v[0], 4*v[1]]                            
        ]),
    NonLinearSystem(
        "tg(xy+0.2)=x^2, x^2+2y^2=1",
        [
            lambda v: tan(v[0]*v[1] + 0.2) - v[0]**2,
            lambda v: v[0]**2 + 2*v[1]**2 - 1
        ],
        lambda v: [
            [v[1]/(cos(v[0]*v[1]+0.2)**2) - 2*v[0], v[0]/(cos(v[0]*v[1]+0.2)**2)],
            [2*v[0], 4*v[1]]
        ] # jacobian
    )
]