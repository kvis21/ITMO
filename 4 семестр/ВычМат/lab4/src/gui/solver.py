# gui/solver.py
import streamlit as st
import math
import methods
from data import SolverState
from gui.input import render_input_section
from gui.graphics import render_plots

def get_r2_interpretation(r2: float) -> str:
    if math.isnan(r2):
        return "Не определено"
    if r2 >= 0.95:
        return "Высокая точность аппроксимации."
    elif r2 >= 0.8:
        return "Хорошая точность аппроксимации."
    elif r2 >= 0.5:
        return "Удовлетворительная точность аппроксимации."
    else:
        return "Неудовлетворительная точность аппроксимации."

def run_gui():
    st.markdown("""
        ### Лабораторная работа №4

        **Выполнил:** студент группы P3215 Панченко А.Д.
    """)

    x_data, y_data, n = render_input_section()
    
    if x_data is None or y_data is None or n == 0:
        st.info("Ожидание корректного набора данных (от 8 до 12 точек) на боковой панели...")
        return

    results = [
        methods.linear_approximation(n, x_data, y_data),
        methods.polynomial_2_approximation(n, x_data, y_data),
        methods.polynomial_3_approximation(n, x_data, y_data),
        methods.exponential_approximation(n, x_data, y_data),
        methods.logarithmic_approximation(n, x_data, y_data),
        methods.power_approximation(n, x_data, y_data)
    ]
    
    best_result = None
    min_delta = float('inf')
    for res in results:
        if res.coefficients is not None and res.delta < min_delta:
            min_delta = res.delta
            best_result = res
            
    state = SolverState(x_data, y_data, n, results, best_result)

    st.markdown("#### Сводные результаты исследования")
    
    table_rows = []
    for res in state.results:
        table_rows.append({
            "Функция": res.name,
            "Статус": res.status,
            "S": f"{res.S:.5f}" if not math.isnan(res.S) else "—",
            "СКО (δ)": f"{res.delta:.5f}" if not math.isnan(res.delta) else "—",
            "R²": f"{res.R2:.5f}" if not math.isnan(res.R2) else "—",
            "Оценка точности (R²)": get_r2_interpretation(res.R2) if not math.isnan(res.R2) else "—"
        })
    st.markdown("""
        <style>
        table th:last-child, table td:last-child {
            max-width: 200px !important;
            white-space: normal !important;
            /*word-wrap: break-word !important;*/
        }
        </style>
    """, unsafe_allow_html=True)
    st.table(table_rows)
    
    linear_res = next((r for r in state.results if r.name == "Линейная"), None)
    if linear_res and linear_res.coefficients is not None:
        st.info(f"**Линейная зависимость:** Коэффициент корреляции Пирсона $r = {linear_res.pearson_r:.4f}$")

    if state.best_result:
        st.success(f"**Наилучшая аппроксимирующая функция:** {state.best_result.name} (минимальное СКО $\delta = {state.best_result.delta:.5f}$)")
        
        coef_str = ", ".join([f"коэф_{i} = {c:.4f}" for i, c in enumerate(state.best_result.coefficients)])
        st.write(f"**Найденные коэффициенты:** `{coef_str}`")
        
        # Пункт 3 ТЗ: Массивы значений x_i, y_i, phi(x_i), eps_i
        st.markdown(f"#### Подробный массив отклонений ({state.best_result.name})")
        best_phi = state.best_result.phi
        epsilon = [best_phi[i] - y_data[i] for i in range(n)]
        
        metrics_df = {
            "№": list(range(1, n + 1)),
            "x_i": state.x_data,
            "y_i": state.y_data,
            "𝜑(x_i)": [round(p, 4) for p in best_phi],
            "𝜺_i (Отклонение)": [round(e, 4) for e in epsilon]
        }
        st.dataframe(metrics_df, use_container_width=True)
        
        render_plots(state.x_data, state.y_data, state.results, state.best_result.name)
    else:
        st.error("Критическая ошибка: ни одна функция не применима для аппроксимации данных.")