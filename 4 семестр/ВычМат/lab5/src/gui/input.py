# gui/input.py
import math
from typing import List, Optional, Tuple

import streamlit as st

FUNCTIONS = {
    "sin(x)": lambda t: math.sin(t),
    "cos(x)": lambda t: math.cos(t),
    "x^3 - 3x + 1": lambda t: t ** 3 - 3 * t + 1,
    "18x/(x^4 + 10)": lambda t: 18 * t / (t ** 4 + 10),
    "e^x / 5": lambda t: math.exp(t) / 5,
}

VARIANT10_X = [2.10, 2.15, 2.20, 2.25, 2.30, 2.35, 2.40]
VARIANT10_Y = [3.7587, 4.1861, 4.9218, 5.3487, 5.9275, 6.4193, 7.0839]


def _parse_numbers(text: str) -> List[float]:
    """Разбирает строку чисел, разделенных пробелами"""
    return [float(v.replace(",", ".")) for v in text.split()]


def _parse_file_lines(lines: List[str]):
    """Разбирает содержимое txt-файла: 1 строка - X, 2 строка - Y."""
    if len(lines) < 2 or not lines[0].strip() or not lines[1].strip():
        raise ValueError("В файле должны быть две строки: первая - X, вторая - Y.")
    x_list = _parse_numbers(lines[0])
    y_list = _parse_numbers(lines[1])
    return x_list, y_list


def render_input_section() -> Tuple[Optional[List[float]], Optional[List[float]], int]:
    """Отрисовывает панель ввода данных"""
    st.sidebar.header("Входные данные")

    input_type = st.sidebar.selectbox(
        "Способ ввода данных:",
        ["Пример", "Ручной ввод", "Из файла", "По функции"],
    )

    x_list, y_list = [], []

    if input_type == "Пример":
        x_list = list(VARIANT10_X)
        y_list = list(VARIANT10_Y)
        st.sidebar.caption("X1 = 2.355, X2 = 2.254")

    elif input_type == "Ручной ввод":
        st.sidebar.subheader("Ручной ввод координат")
        x_str = st.sidebar.text_area("Вектор X (через пробел):",
                                     "2.10 2.15 2.20 2.25 2.30 2.35 2.40")
        y_str = st.sidebar.text_area("Вектор Y (через пробел):",
                                     "3.7587 4.1861 4.9218 5.3487 5.9275 6.4193 7.0839")
        try:
            x_list = _parse_numbers(x_str)
            y_list = _parse_numbers(y_str)
        except ValueError:
            st.sidebar.error("Ошибка! Проверьте корректность введенных чисел.")
            return None, None, 0

    elif input_type == "Из файла":
        st.sidebar.subheader("Загрузка данных из файла")
        st.sidebar.caption("Формат: 1 строка - X, 2 строка - Y")
        uploaded_file = st.sidebar.file_uploader("Выберите файл")
        if uploaded_file is not None:
            try:
                lines = uploaded_file.read().decode("utf-8").splitlines()
                x_list, y_list = _parse_file_lines(lines)
                st.sidebar.success(f"Загружен файл {uploaded_file.name}")
            except Exception as e:
                st.sidebar.error(f"Не удалось прочитать файл: {e}")
                return None, None, 0
        else:
            st.sidebar.info("Загрузите файл с данными.")
            return None, None, 0

    elif input_type == "По функции":
        st.sidebar.subheader("Генерация по функции")
        func_name = st.sidebar.selectbox("Функция:", list(FUNCTIONS.keys()))
        a = st.sidebar.number_input("Начало интервала a:", value=0.0, format="%.4f")
        b = st.sidebar.number_input("Конец интервала b:", value=1.0, format="%.4f")
        n_points = st.sidebar.slider("Количество точек:", 2, 15, 7)
        if b <= a:
            st.sidebar.error("Конец интервала должен быть больше начала.")
            return None, None, 0
        f = FUNCTIONS[func_name]
        h = (b - a) / (n_points - 1)
        x_list = [round(a + i * h, 6) for i in range(n_points)]
        try:
            y_list = [round(f(x), 4) for x in x_list]
        except Exception as e:
            st.sidebar.error(f"Ошибка при вычислении функции: {e}")
            return None, None, 0
        st.sidebar.success(f"Сгенерированы {n_points} точек по функции {func_name}")

    n = len(x_list)
    if n == 0 or len(y_list) == 0:
        return None, None, 0
    if n != len(y_list):
        st.sidebar.error(f"Размеры не совпадают! X: {n}, Y: {len(y_list)}")
        return None, None, 0

    st.sidebar.write("**Входная таблица:**")
    st.sidebar.dataframe({"x_i": x_list, "y_i": y_list}, height=280)
    return x_list, y_list, n
