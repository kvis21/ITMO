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
    # Якобиан возвращает матрицу 2x2 в виде списка списков [[a, b], [c, d]]
    jacobian: Callable[[List[float]], List[List[float]]]

    def __str__(self) -> str:
        return self.func_str

# Примеры заполнения (добавьте свои из таблицы)
EQUATIONS = [
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
        "tg(xy+0.2)=x^2, x^2+2y^2=1",
        [
            lambda v: tan(v[0]*v[1] + 0.2) - v[0]**2,
            lambda v: v[0]**2 + 2*v[1]**2 - 1
        ],
        lambda v: [
            [v[1]/(cos(v[0]*v[1]+0.2)**2) - 2*v[0], v[0]/(cos(v[0]*v[1]+0.2)**2)],
            [2*v[0], 4*v[1]]
        ]
    )
]