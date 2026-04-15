import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, List, Tuple, Optional
import pandas as pd

# --- 1. Математические модели (Уравнения и Системы) ---

class NonlinearEquation:
    def __init__(self, name: str, func: Callable, deriv: Callable, second_deriv: Callable, phi: Callable = None):
        self.name = name
        self.f = func
        self.df = deriv
        self.ddf = second_deriv
        self.phi = phi  # Для метода простой итерации x = phi(x)

class NonlinearSystem:
    def __init__(self, name: str, funcs: List[Callable], jacobian: Callable, phi: Callable = None):
        self.name = name
        self.funcs = funcs
        self.jacobian = jacobian
        self.phi = phi # Для метода простой итерации X = Phi(X)

# Предустановленные данные
EQUATIONS = [
    NonlinearEquation("x^3 - x + 4 = 0", lambda x: x**3 - x + 4, lambda x: 3*x**2 - 1, lambda x: 6*x),
    NonlinearEquation("sin(x) + 0.1 = x^2", lambda x: np.sin(x) + 0.1 - x**2, lambda x: np.cos(x) - 2*x, lambda x: -np.sin(x) - 2),
    NonlinearEquation("e^x - 2 = 0", lambda x: np.exp(x) - 2, lambda x: np.exp(x), lambda x: np.exp(x))
]

# Системы из вашего задания
SYSTEMS = [
    # №11 (Метод Ньютона)
    NonlinearSystem("№11: tg(xy+0.2)=x^2, x^2+2y^2=1", 
        [lambda v: np.tan(v[0]*v[1] + 0.2) - v[0]**2, lambda v: v[0]**2 + 2*v[1]**2 - 1],
        lambda v: np.array([
            [v[1]/(np.cos(v[0]*v[1]+0.2)**2) - 2*v[0], v[0]/(np.cos(v[0]*v[1]+0.2)**2)],
            [2*v[0], 4*v[1]]
        ])),
    # №12 (Метод простой итерации)
    NonlinearSystem("№12: x + sin(y) = -0.4, 2y - cos(x+1) = 0",
        [lambda v: v[0] + np.sin(v[1]) + 0.4, lambda v: 2*v[1] - np.cos(v[0] + 1)],
        None,
        phi=lambda v: np.array([-np.sin(v[1]) - 0.4, 0.5 * np.cos(v[0] + 1)]))
]

# --- 2. Численные методы (Логика) ---

def solve_newton_scalar(eq: NonlinearEquation, a: float, b: float, eps: float):
    # Выбор начального приближения (условие f(x0)*f''(x0) > 0)
    x = a if eq.f(a) * eq.ddf(a) > 0 else b
    iters = 0
    while iters < 100:
        fx = eq.f(x)
        dfx = eq.df(x)
        x_next = x - fx / dfx
        iters += 1
        if abs(x_next - x) < eps:
            return x_next, iters, fx
        x = x_next
    return x, iters, eq.f(x)

def solve_newton_system(sys: NonlinearSystem, x0: np.ndarray, eps: float):
    x = x0.astype(float)
    history = []
    for i in range(100):
        f_val = np.array([f(x) for f in sys.funcs])
        j_val = sys.jacobian(x)
        delta = np.linalg.solve(j_val, -f_val)
        x_new = x + delta
        diff = np.abs(delta)
        history.append(diff)
        if np.max(diff) < eps:
            return x_new, i + 1, history
        x = x_new
    return x, 100, history

# --- 3. Streamlit Интерфейс ---

st.set_page_config(page_title="ВычМат: Нелинейные уравнения", layout="wide")
st.title("Решение нелинейных уравнений и систем")

task_type = st.sidebar.selectbox("Выберите тип задачи:", ["Уравнение", "Система уравнений"])

if task_type == "Уравнение":
    selected_eq = st.selectbox("Выберите уравнение:", EQUATIONS, format_func=lambda x: x.name)
    
    col1, col2 = st.columns(2)
    with col1:
        input_method = st.radio("Ввод данных:", ["Клавиатура", "Файл"])
        if input_method == "Клавиатура":
            a = st.number_input("Граница a", value=-2.0)
            b = st.number_input("Граница b", value=2.0)
            eps = st.number_input("Погрешность", value=0.01, format="%.4f")
        else:
            uploaded_file = st.file_uploader("Загрузите файл (a, b, eps)")
            if uploaded_file:
                data = uploaded_file.read().decode().split()
                a, b, eps = map(float, data)
            else: st.stop()

    # Верификация корня
    if selected_eq.f(a) * selected_eq.f(b) > 0:
        st.error("На данном интервале нет корней или их четное количество (условие f(a)*f(b) < 0 не выполнено)")
    else:
        method_name = st.selectbox("Метод решения:", ["Ньютона", "Секущих", "Простой итерации"])
        
        if st.button("Рассчитать"):
            # Тут вызов соответствующего метода
            res, iters, f_val = solve_newton_scalar(selected_eq, a, b, eps)
            
            st.success(f"Результат найден!")
            st.write(f"**Корень:** {res:.6f}")
            st.write(f"**Значение функции:** {f_val:.2e}")
            st.write(f"**Итераций:** {iters}")
            
            # График
            fig, ax = plt.subplots()
            x_vals = np.linspace(a - 1, b + 1, 400)
            ax.plot(x_vals, [selected_eq.f(val) for val in x_vals], label="f(x)")
            ax.axhline(0, color='black', lw=1)
            ax.scatter([res], [0], color='red', zorder=5, label="Корень")
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)

else:  # СИСТЕМЫ
    selected_sys = st.selectbox("Выберите систему:", SYSTEMS, format_func=lambda x: x.name)
    
    st.info("Метод решения для этой системы предопределен таблицей.")
    
    col1, col2 = st.columns(2)
    with col1:
        x0_1 = st.number_input("Начальное x1", value=0.5)
        x0_2 = st.number_input("Начальное x2", value=0.5)
        eps_sys = st.number_input("Погрешность", value=0.001, format="%.4f")
    
    if st.button("Решить систему"):
        res, iters, history = solve_newton_system(selected_sys, np.array([x0_1, x0_2]), eps_sys)
        
        st.subheader("Результаты:")
        st.write(f"Вектор неизвестных: **X = {res}**")
        st.write(f"Количество итераций: **{iters}**")
        
        st.write("Вектор погрешностей на последнем шаге:")
        st.write(history[-1])

        fig, ax = plt.subplots()
        x_range = np.linspace(res[0]-2, res[0]+2, 100)
        y_range = np.linspace(res[1]-2, res[1]+2, 100)
        X, Y = np.meshgrid(x_range, y_range)
        
        Z1 = np.array([[selected_sys.funcs[0]([x, y]) for x in x_range] for y in y_range])
        Z2 = np.array([[selected_sys.funcs[1]([x, y]) for x in x_range] for y in y_range])
        
        ax.contour(X, Y, Z1, levels=[0], colors='blue')
        ax.contour(X, Y, Z2, levels=[0], colors='green')
        ax.scatter([res[0]], [res[1]], color='red', label="Решение")
        ax.grid(True)
        st.pyplot(fig)