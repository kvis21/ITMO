from math import log, tanh, sin, cos, cosh
import pandas as pd

EPSILON = 1e-8
f = lambda x: 1.691 * (tanh(sin(3*x)) * cos(2*x))
df = lambda x: (5073*cos(2*x)*cos(3*x))/(1000*cosh(sin(3*x))**2)-(1691*sin(2*x)*tanh(sin(3*x)))/(500)
borders = [0, 1]

def hord_method (a, b, eps = 0.01, minimum = True) -> pd.DataFrame:
    iterations = []
    step = 1

    sign = 1 if minimum else -1
    while True:
        c = a - (df(a) / (df(a) - df(b))) * (a - b)
        dc = df(c)

        if abs(dc) < eps:
            break
            
        if dc > 0:
            b = c
        elif dc < 0:
            a = c

        iterations.append({"iter": step, "a": a, "b": b, "c": c, "f(c)":f(c), "df(c)": dc})
        step += 1
    return pd.DataFrame(iterations)

if __name__ == "__main__":
    data_min = hord_method(*borders, eps=EPSILON, minimum=True)
    data_max = hord_method(*borders, eps=EPSILON, minimum=False)

    print(data_min)
    print(data_max)
    print("Minimum:")
    print("точка минимума: ", data_min.iloc[-1]["c"])
    print("число итераций: ", len(data_min))
    print("Maximum:")
    print("точка максимума: ", data_max.iloc[-1]["c"])
    print("число итераций: ", len(data_max))

    




#