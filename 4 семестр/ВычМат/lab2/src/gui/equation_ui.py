import streamlit as st
import pandas as pd
from gui.input_ui import render_equation_input
from method_manager import MethodManager
from methods.base import MethodType

from util.graph_util import create_equation_plot 

def render_equation_page(equations):
    data = render_equation_input(equations)
    
    if not data:
        st.session_state.pop('eq_result', None)
        return

    eq, a, b, eps = data["equation"], data["a"], data["b"], data["eps"]
    max_iter = data["max_iter"]

    method_type = st.selectbox(
        "Выберите метод решения:", 
        [MethodType.SIMPLE_ITERATION, MethodType.CHORD, MethodType.SECANT],
        format_func=lambda x: x.value
    )

    current_state_id = f"{eq.func_str}_{a}_{b}_{eps}_{method_type.name}"

    if st.session_state.get('last_eq_id') != current_state_id:
        st.session_state.pop('eq_result', None)
        st.session_state['last_eq_id'] = current_state_id

    try:
        if st.button("Найти корень", type="primary"):
            if eq.f(a) * eq.f(b) > 0:
                st.error("Ошибка: f(a) и f(b) имеют одинаковые знаки. На отрезке может не быть корней или их четное количество.")
                st.session_state.pop('eq_result', None)
            else:
                solver = MethodManager.get_method(method_type)
                x0 = a if eq.f(a) * eq.ddf(a) > 0 else b
                st.session_state['eq_result'] = solver.solve(eq, x0=x0, a=a, b=b, eps=eps, max_iter=max_iter)
                st.rerun()
    except OverflowError:
        st.error("Ошибка переполнения (OverflowError): значения стали слишком велики. Возможно, метод расходится для данной функции или начального приближения.")
        st.session_state.pop('eq_result', None)
    except Exception as e:
        st.error(f"Произошла непредвиденная ошибка: {e}")
        st.session_state.pop('eq_result', None)


    """
    секция с выводом результатов
    """
    if 'eq_result' in st.session_state:
        result = st.session_state['eq_result']
        
        if not result.success:
            st.error(f"Расчет не удался: {result.error_message}")
        else:
            st.divider()
            st.success(f"Корень найден: **{result.solutions[0]:.6f}**")
            
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Итераций", len(result.iterations_data))
            col_m2.metric("f(x)", f"{eq.f(result.solutions[0]):.2e}")
            col_m3.metric("Погрешность", f"{result.errors[0]:.2e}")

            st.subheader("Таблица итераций")
            df = pd.DataFrame(
                result.iterations_data, 
                columns=["№", "x_n", "f(x_n)", "Погрешность"]
            )
            st.dataframe(df, use_container_width=True)

            st.subheader("Визуализация")
            try:
                fig = create_equation_plot(eq, a, b, result.solutions[0])
                st.plotly_chart(fig, use_container_width=True, theme=None)
            except Exception as e:
                st.warning(f"Не удалось построить график: {e}")