from math import log, tanh, sin, cos, cosh, log2
import pandas as pd
from typing import Tuple

DELTA = 0.01
EPSILON = 1e-8
f = lambda x: 1.691 * (tanh(sin(3*x)) * cos(2*x))
borders = [0, 1]

def half_division_method(a, b, eps = EPSILON) -> Tuple[pd.DataFrame, int]:
    step = 0
    delta = eps
    iterations = []
    while (b - a) / 2 > eps:
        c = (b + a) / 2
        x_1 = c-delta
        x_2 = c+delta

        if f(x_1) < f(x_2): b = c
        else: a = c

        step += 1
        iterations.append({"iter": step, "a": a, "b": b, "c": c, "f(c)":f(c)})
    teor_iter = log2((b-a-delta)/(2*eps-delta))
    return pd.DataFrame(iterations), teor_iter

data, teor_iter = half_division_method(*borders)

print("количество итераций фактическое:", len(data))
print("количество итераций теоретическое:", teor_iter)


