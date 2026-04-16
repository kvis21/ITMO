import streamlit as st
from typing import Optional

def render_equation_input(equations: list) -> Optional[dict]:
    st.subheader("Настройка параметров уравнения")
    
    # Используем key, чтобы Streamlit запоминал выбор при перезагрузке
    selected_eq = st.selectbox(
        "Выберите уравнение:", 
        equations, 
        format_func=lambda x: x.func_str,
        key="eq_selector"
    )

    input_method = st.radio("Источник данных:", ["Клавиатура", "Файл"], key="eq_mode")
    
    a, b, eps = None, None, None

    if input_method == "Клавиатура":
        col1, col2, col3 = st.columns(3)
        # Значения по умолчанию берем из параметров, чтобы не обнулялись
        a = col1.number_input("Левая граница (a)", value=-1.0, format="%.4f", key="eq_a")
        b = col2.number_input("Правая граница (b)", value=1.0, format="%.4f", key="eq_b")
        eps = col3.number_input("Точность (eps)", value=0.0001, format="%.6f", key="eq_eps")
    else:
        uploaded_file = st.file_uploader("Загрузите файл (a b eps)", key="eq_file")
        if uploaded_file:
            try:
                content = uploaded_file.read().decode().strip().split()
                if len(content) == 3:
                    a, b, eps = map(float, content)
                    st.success(f"Загружено: a={a}, b={b}, eps={eps}")
                else:
                    st.error("В файле должно быть 3 числа.")
            except Exception:
                st.error("Ошибка чтения файла.")
        
    # КРИТИЧЕСКИЙ МОМЕНТ: 
    # Если данные не введены (особенно для файла), мы просто выводим инфо, 
    # но не даем основной логике упасть
    if a is None or b is None or eps is None:
        st.info("Ожидание ввода параметров...")
        return None

    if a >= b:
        st.warning("Граница 'a' должна быть меньше 'b'.")
        return None
        
    return {"equation": selected_eq, "a": a, "b": b, "eps": eps}

def render_system_input(systems: list) -> Optional[dict]:
    st.subheader("Настройка параметров системы")
    
    # ВАЖНО: Убираем st.form, если он мешает мгновенному сохранению состояния.
    # Для систем лучше использовать обычные поля с ключами.
    selected_sys = st.selectbox(
        "Выберите систему:", 
        systems, 
        format_func=lambda x: x.func_str,
        key="sys_selector"
    )

    st.info("Введите начальные приближения")
    col1, col2, col3 = st.columns(3)
    x1_0 = col1.number_input("Начальное x1", value=0.1, key="sys_x1")
    x2_0 = col2.number_input("Начальное x2", value=0.1, key="sys_x2")
    eps = col3.number_input("Точность", value=0.001, key="sys_eps")

    return {
        "system": selected_sys,
        "x0": [x1_0, x2_0],
        "eps": eps
    }