import streamlit as st
from typing import Optional
from equation import NonLinearSystem, NonLinearEquation

def render_equation_input(equations: list[NonLinearEquation]) -> Optional[dict]:
    st.subheader("Настройка параметров уравнения")
    
    # Используем key, чтобы Streamlit запоминал выбор при перезагрузке
    selected_eq = st.selectbox(
        "Выберите уравнение:", 
        equations, 
        format_func=lambda x: x.func_str,
        key="eq_selector"
    )

    input_method = st.radio("Источник данных:", ["Клавиатура", "Файл"], key="eq_mode")
    
    a, b, eps, max_iter = None, None, None, 100

    if input_method == "Клавиатура":
        col1, col2, col3, col4 = st.columns(4)
        # Значения по умолчанию берем из параметров, чтобы не обнулялись
        a = col1.number_input("Левая граница (a)", value=-1.0, format="%.4f", key="eq_a")
        b = col2.number_input("Правая граница (b)", value=1.0, format="%.4f", key="eq_b")
        eps = col3.number_input("Точность (eps)", value=0.0001, format="%.6f", key="eq_eps")
        max_iter = col4.number_input("Макс. итераций", min_value=1, value=100, step=10, key="eq_iter")
    else:
        uploaded_file = st.file_uploader("Загрузите файл (a b eps)", key="eq_file")
        if uploaded_file:
            try:
                content = uploaded_file.read().decode().strip().split()
                if len(content):
                    a, b, eps = map(float, content)
                    st.success(f"Загружено: a={a}, b={b}, eps={eps}")
                else:
                    st.error("В файле должно быть 3 числа: a, b, eps.")
            except Exception:
                st.error("Ошибка чтения файла.")

    if a is None or b is None or eps is None:
        st.info("Ожидание ввода параметров...")
        return None
    if a >= b:
        st.warning("Граница 'a' должна быть меньше 'b'.")
        return None
        
    return {"equation": selected_eq, "a": a, "b": b, "eps": eps, "max_iter": max_iter}

def render_system_input(systems: list[NonLinearSystem]) -> Optional[dict]:
    st.subheader("Настройка параметров системы")
    
    selected_sys = st.selectbox(
        "Выберите систему:", 
        systems, 
        format_func=lambda x: x.func_str,
        key="sys_selector"
    )

    st.info("Введите начальные приближения")
    col1, col2, col3, col4 = st.columns(4)
    x1_0 = col1.number_input("Начальное x1", value=0.1, key="sys_x1")
    x2_0 = col2.number_input("Начальное x2", value=0.1, key="sys_x2")
    eps = col3.number_input("Точность", value=0.001, key="sys_eps")
    max_iter = col4.number_input("Макс. итераций", min_value=1, value=100, step=10, key="sys_iter")

    return {
        "system": selected_sys, 
        "x0": [x1_0, x2_0], 
        "eps": eps, 
        "max_iter": max_iter
    }