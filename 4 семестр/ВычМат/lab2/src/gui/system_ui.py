import streamlit as st
import pandas as pd
from gui.input_ui import render_system_input
from method_manager import MethodManager
from methods.base import MethodType

from util.graph_util import create_system_plot

def render_system_page(systems):
    data = render_system_input(systems)
    if not data: 
        st.session_state.pop('sys_result', None)
        return

    sys_obj, x0, eps, max_iter = data["system"], data["x0"], data["eps"], data['max_iter']

    current_input_id = f"{sys_obj.func_str}_{x0}_{eps}_{max_iter}"
    
    if st.session_state.get('last_input_id') != current_input_id:
        st.session_state.pop('sys_result', None)
        st.session_state['last_input_id'] = current_input_id

    try:
        if st.button("Решить СНЛАУ", type="primary"):
            solver = MethodManager.get_method(MethodType.NEWTON)
            st.session_state['sys_result'] = solver.solve(sys_obj, x0=x0, eps=eps, max_iter=max_iter)
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
    if 'sys_result' in st.session_state:
        result = st.session_state['sys_result']
        
        if result.success:
            st.success("Решение успешно найдено!")
            
            col_r1, col_r2, col_r3 = st.columns(3)
            col_r1.metric("x1", f"{result.solutions[0]:.6f}")
            col_r2.metric("x2", f"{result.solutions[1]:.6f}")
            col_r3.metric("Итераций", len(result.iterations_data))

            st.subheader("Ход решения")
            df = pd.DataFrame(
                result.iterations_data, 
                columns=["№", "x1", "x2", "Погрешность"]
            )
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.subheader("Визуализация системы")
            try:
                fig = create_system_plot(sys_obj, result.solutions[0], result.solutions[1])
                st.plotly_chart(fig, use_container_width=True, theme=None)
            except Exception as e:
                st.warning(f"Не удалось построить график: {e}")
            
        else:
            st.error(f"Ошибка: {result.error_message}")