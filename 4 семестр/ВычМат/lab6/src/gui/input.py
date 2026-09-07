import math
from typing import Optional, Tuple

import streamlit as st

from data import ODE

ODES = [
    ODE(
        name="y' = -y",
        f=lambda x, y: -y,
        exact=lambda x: math.exp(-x),
        x0=0.0, y0=1.0, xn=2.0, h=0.1,
        formula="y' = -y,  y(0) = 1,  yточн = e^(-x)",
    ),
    ODE(
        name="y' = y",
        f=lambda x, y: y,
        exact=lambda x: math.exp(x),
        x0=0.0, y0=1.0, xn=1.0, h=0.1,
        formula="y' = y,  y(0) = 1,  yточн = e^x",
    ),
    ODE(
        name="y' = -2xy",
        f=lambda x, y: -2 * x * y,
        exact=lambda x: math.exp(-x ** 2),
        x0=0.0, y0=1.0, xn=2.0, h=0.1,
        formula="y' = -2xy,  y(0) = 1,  yточн = e^(-x²)",
    ),
    ODE(
        name="y' = x + y",
        f=lambda x, y: x + y,
        exact=lambda x: 2 * math.exp(x) - x - 1,
        x0=0.0, y0=1.0, xn=1.0, h=0.1,
        formula="y' = x + y,  y(0) = 1,  yточн = 2e^x - x - 1",
    ),
    ODE(
        name="y' = y(1 - y)",
        f=lambda x, y: y * (1 - y),
        exact=lambda x: math.exp(x) / (math.exp(x) + 1),
        x0=0.0, y0=0.5, xn=3.0, h=0.1,
        formula="y' = y(1 - y),  y(0) = 0.5,  yточн = e^x / (e^x + 1)",
    ),
]


def render_input_section() -> Tuple[Optional[ODE], float, float]:
    st.sidebar.header("Входные данные")

    ode_names = [o.name for o in ODES]
    selected = st.sidebar.selectbox("Выберите ОДУ:", ode_names)
    ode = next(o for o in ODES if o.name == selected)

    st.sidebar.caption(ode.formula)

    st.sidebar.subheader("Параметры")
    x0 = st.sidebar.number_input("Начало интервала x₀:", value=ode.x0, format="%.4f")
    xn = st.sidebar.number_input("Конец интервала xₙ:", value=ode.xn, format="%.4f")
    h = st.sidebar.number_input("Шаг h:", value=ode.h, min_value=0.001, format="%.4f")
    eps = st.sidebar.number_input("Точность ε:", value=0.001, min_value=0.0001, format="%.6f")

    if xn <= x0:
        st.sidebar.error("Конец интервала должен быть больше начала.")
        return None, h, eps

    if h <= 0:
        st.sidebar.error("Шаг должен быть положительным.")
        return None, h, eps

    return ode, h, eps
