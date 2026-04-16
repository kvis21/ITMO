import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from gui.input_ui import render_equation_input
from method_manager import MethodManager
from methods.base import MethodType

def render_equation_page(equations):
    # 1. Получаем ввод
    data = render_equation_input(equations)
    
    st.write(f"DEBUG: Data received: {data is not None}")
    if not data:
        st.session_state.pop('eq_result', None)
        st.write("DEBUG: EXITING DUE TO EMPTY DATA")
        return


    eq, a, b, eps = data["equation"], data["a"], data["b"], data["eps"]

    # 2. Выбор метода
    method_type = st.selectbox(
        "Выберите метод решения:", 
        [MethodType.SIMPLE_ITERATION, MethodType.CHORD, MethodType.SECANT],
        format_func=lambda x: x.value
    )

    # Идентификатор текущего состояния ввода для сброса старых результатов
    current_state_id = f"{eq.func_str}_{a}_{b}_{eps}_{method_type.name}"

    if st.session_state.get('last_eq_id') != current_state_id:
        st.session_state.pop('eq_result', None)
        st.session_state['last_eq_id'] = current_state_id

    # 3. Кнопка расчета
    if st.button("Найти корень", type="primary"):
        # Валидация наличия корня перед расчетом
        if eq.f(a) * eq.f(b) > 0:
            st.error("Ошибка: f(a) и f(b) имеют одинаковые знаки. На отрезке может не быть корней или их четное количество.")
            st.session_state.pop('eq_result', None)
        else:
            solver = MethodManager.get_method(method_type)
            
            x0 = a if eq.f(a) * eq.ddf(a) > 0 else b
            
            # Решаем и сохраняем в сессию
            st.session_state['eq_result'] = solver.solve(eq, x0=x0, a=a, b=b, eps=eps)
            st.rerun()

    # 4. Блок отрисовки (работает всегда, если есть данные в сессии)
    if 'eq_result' in st.session_state:
        result = st.session_state['eq_result']
        
        if not result.success:
            st.error(f"Расчет не удался: {result.error_message}")
        else:
            st.divider()
            st.success(f"Корень найден: **{result.solutions[0]:.6f}**")
            
            # Метрики для красоты
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Итераций", len(result.iterations_data))
            col_m2.metric("f(x)", f"{eq.f(result.solutions[0]):.2e}")
            col_m3.metric("Погрешность", f"{result.errors[0]:.2e}")

            # Таблица итераций
            st.subheader("Таблица итераций")
            df = pd.DataFrame(
                result.iterations_data, 
                columns=["№", "x_n", "f(x_n)", "Погрешность"]
            )
            st.dataframe(df, use_container_width=True)

            # График функции
            st.subheader("Визуализация")
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Генерируем точки для графика (без numpy здесь сложно, 
            # но для визуализации в GUI он обычно допустим)
            import numpy as np
            margin = (b - a) * 0.2
            x_range = np.linspace(a - margin, b + margin, 500)
            y_range = [eq.f(x) for x in x_range]
            
            ax.plot(x_range, y_range, label=f"f(x) = {eq.func_str}", color="#1f77b4")
            ax.axhline(0, color='black', lw=1)
            ax.axvline(0, color='black', lw=1)
            
            # Выделяем отрезок [a, b]
            ax.axvspan(a, b, color='gray', alpha=0.1, label="Отрезок поиска")
            
            # Точка корня
            ax.scatter(result.solutions, [0], color='red', s=100, label="Корень", zorder=5)
            
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend()
            st.pyplot(fig)