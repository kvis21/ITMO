import streamlit as st
from typing import Optional

import methods
from data import MethodResult, ODE, SolverState
from gui.graphics import render_plots
from gui.input import render_input_section
from utils import exact_max_error, runge_rule


def run_gui():
    st.markdown("### Лабораторная работа №6")
    st.markdown("**Численное решение обыкновенных дифференциальных уравнений**")
    st.markdown("Выполнил: студент группы P3215 Панченко А.Д.")

    ode, h, eps = render_input_section()

    if ode is None:
        st.info("Выберите ОДУ и параметры на боковой панели.")
        return

    st.markdown("#### Исходное ОДУ")
    st.latex(ode.formula)

    col1, col2, col3 = st.columns(3)
    col1.metric("x₀", f"{ode.x0:.4f}")
    col2.metric("xₙ", f"{xn:.4f}" if (xn := ode.xn) else "—")
    col3.metric("Шаг h", f"{h:.4f}")

    results = []

    x_e, y_e = methods.euler(ode.f, ode.x0, ode.y0, ode.xn, h)
    y_exact_e = [ode.exact(xi) for xi in x_e] if ode.exact else None
    err_e = exact_max_error(y_e, y_exact_e) if y_exact_e else None
    runge_e = runge_rule(ode.f, ode.x0, ode.y0, ode.xn, h, 1, methods.euler)
    results.append(MethodResult("Метод Эйлера", x_e, y_e, "Успешно", err_e, runge_e))

    x_rk, y_rk = methods.runge_kutta_4(ode.f, ode.x0, ode.y0, ode.xn, h)
    y_exact_rk = [ode.exact(xi) for xi in x_rk] if ode.exact else None
    err_rk = exact_max_error(y_rk, y_exact_rk) if y_exact_rk else None
    runge_rk = runge_rule(ode.f, ode.x0, ode.y0, ode.xn, h, 4, methods.runge_kutta_4)
    results.append(MethodResult("Рунге-Кутта 4", x_rk, y_rk, "Успешно", err_rk, runge_rk))

    x_ml, y_ml = methods.milne(ode.f, ode.x0, ode.y0, ode.xn, h)
    y_exact_ml = [ode.exact(xi) for xi in x_ml] if ode.exact else None
    err_ml = exact_max_error(y_ml, y_exact_ml) if y_exact_ml else None
    results.append(MethodResult("Милн", x_ml, y_ml, "Успешно", err_ml, None))

    st.markdown("#### Таблица результатов")
    table_data = []
    for r in results:
        row = {
            "Метод": r.name,
            "Порядок": "O(h)" if "Эйлер" in r.name else "O(h⁴)",
            "Погрешность ε": f"{r.error:.6e}" if r.error is not None else "—",
            "Правило Рунге R": f"{r.runge_error:.6e}" if r.runge_error is not None else "—",
            "Статус": r.status,
        }
        table_data.append(row)
    st.dataframe(table_data, use_container_width=True, hide_index=True)

    if ode.exact:
        st.markdown("#### Таблица значений (сравнение с точным решением)")
        all_x = set()
        for r in results:
            all_x.update(r.x)
        all_x = sorted(all_x)

        table_values = []
        for xi in all_x:
            row = {"x": f"{xi:.4f}"}
            y_ex = ode.exact(xi)
            row["Точное"] = f"{y_ex:.6f}"
            for r in results:
                idx = r.x.index(xi) if xi in r.x else None
                if idx is not None:
                    row[r.name] = f"{r.y[idx]:.6f}"
                else:
                    row[r.name] = "—"
            table_values.append(row)
        st.dataframe(table_values, use_container_width=True, hide_index=True)

    st.markdown("#### Графики решений")
    if ode.exact:
        x_plot, y_plot = methods.runge_kutta_4(ode.f, ode.x0, ode.y0, ode.xn, h / 10)
        y_exact_plot = [ode.exact(xi) for xi in x_plot]
        st.plotly_chart(render_plots(x_plot, y_exact_plot, results, ode.name),
                        use_container_width=True)
    else:
        st.plotly_chart(render_plots([], [], results, ode.name),
                        use_container_width=True)
