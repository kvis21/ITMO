# gui/solver.py
import math
from typing import List

import streamlit as st

import methods
from data import InterpolationResult, SolverState
from gui.graphics import render_plots
from gui.input import render_input_section
from utils import (build_divided_difference_table, build_finite_difference_table,
                   check_equidistant, validate_data)

_SUPERSCRIPT = "⁰¹²³⁴⁵⁶⁷⁸⁹"


def _superscript(k: int) -> str:
    return "".join(_SUPERSCRIPT[int(d)] for d in str(k))


def _round(v) -> float:
    return round(v, 6)


def _render_table_dataframe(x_list: List[float], y_list: List[float], kind: str):
    """Выводит таблицу конечных или разделенных разностей."""
    if kind == "finite":
        table = build_finite_difference_table(y_list)
        title = "#### Таблица конечных разностей"
        labels = ["y"] + [f"Δ{_superscript(k)}y" for k in range(1, len(table))]
    else:
        table = build_divided_difference_table(x_list, y_list)
        title = "#### Таблица разделенных разностей"
        labels = ["f[x_i]"]
        for k in range(1, len(table)):
            labels.append(f"f[x_i…x_{{{'i+' + str(k)}}}]")

    n = len(x_list)
    data = []
    for i in range(n):
        row = {"x": x_list[i]}
        for k, col in enumerate(table):
            row[labels[k]] = _round(col[i]) if i < len(col) else None
        data.append(row)

    st.markdown(title)
    st.caption("Треугольная таблица разностей. Пустые ячейки соответствуют несуществующим разностям.")
    st.dataframe(data, use_container_width=True, hide_index=True)


def _render_finite_table(x_list, y_list):
    ok, h = check_equidistant(x_list)
    if ok:
        _render_table_dataframe(x_list, y_list, "finite")
        st.caption(f"Шаг интерполяции h = {h} — узлы равноотстоящие, конечные разности применимы.")
    else:
        st.warning("Узлы не являются равноотстоящими: конечные разности и формулы Ньютона/Гаусса "
                   "с конечными разностями неприменимы для этих данных.")


def _render_divided_table(x_list, y_list):
    _render_table_dataframe(x_list, y_list, "divided")


def _compute_all(x: float, x_list: List[float], y_list: List[float]) -> List[InterpolationResult]:
    results = []
    for desc in methods.all_methods():
        results.append(desc["func"](x, x_list, y_list))
    return results


def run_gui():
    st.markdown("### Лабораторная работа №5")
    st.markdown("**Интерполяция функции**")
    st.markdown("Выполнил: студент группы P3215 Панченко А.Д.")

    x_list, y_list, n = render_input_section()

    if x_list is None or n == 0:
        st.info("Ожидание корректного набора данных (минимум 2 точки) на боковой панели...")
        return

    errors = validate_data(x_list, y_list)
    if errors:
        for e in errors:
            st.error(e)
        return

    st.markdown("#### Исходные данные")
    st.dataframe({"x_i": x_list, "y_i": y_list}, use_container_width=True, hide_index=True)

    _render_finite_table(x_list, y_list)
    _render_divided_table(x_list, y_list)

    x_min, x_max = min(x_list), max(x_list)
    default_x = round((x_min + x_max) / 2, 4)
    x = st.number_input("Аргумент интерполяции X:", value=default_x,
                        min_value=None, max_value=None, step=0.001, format="%.4f")
    if x < x_min or x > x_max:
        st.warning("Точка X находится вне отрезка [x0, xn] — выполняется экстраполяция.")

    results = _compute_all(x, x_list, y_list)
    state = SolverState(x_list, y_list, n, x, results)

    st.markdown(f"#### Результаты вычисления значения функции при X = {x:.4f}")
    table_rows = []
    for r in state.results:
        table_rows.append({
            "Метод": r.name,
            "y(X)": f"{r.value:.6f}" if r.value is not None else "—",
            "Статус": r.status,
            "Примененная формула": r.formula or "—",
        })
    st.dataframe(table_rows, use_container_width=True, hide_index=True)

    ok_results = [r for r in state.results if r.value is not None]
    if ok_results:
        st.plotly_chart(render_plots(x_list, y_list, results, x), use_container_width=True)
    else:
        st.error("Ни один метод не смог вычислить значение функции.")
