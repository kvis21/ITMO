import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from gui.input_ui import render_system_input
from method_manager import MethodManager
from methods.base import MethodType

def render_system_page(systems):
    data = render_system_input(systems)
    if not data: 
        st.session_state.pop('sys_result', None)
        return

    sys_obj, x0, eps, max_iter = data["system"], data["x0"], data["eps"], data['max_iter']

    # Идентификатор для сброса (добавили max_iter для точности)
    current_input_id = f"{sys_obj.func_str}_{x0}_{eps}_{max_iter}"
    
    if st.session_state.get('last_input_id') != current_input_id:
        st.session_state.pop('sys_result', None)
        st.session_state['last_input_id'] = current_input_id

    if st.button("Решить СНЛАУ", type="primary"):
        solver = MethodManager.get_method(MethodType.NEWTON)
        st.session_state['sys_result'] = solver.solve(sys_obj, x0=x0, eps=eps, max_iter=max_iter)
        st.rerun() 
        
    if 'sys_result' in st.session_state:
        result = st.session_state['sys_result']
        
        if result.success:
            st.success("Решение успешно найдено!")
            
            # --- БЛОК ВЫВОДА МЕТРИК ---
            col_r1, col_r2, col_r3 = st.columns(3)
            col_r1.metric("x1", f"{result.solutions[0]:.6f}")
            col_r2.metric("x2", f"{result.solutions[1]:.6f}")
            col_r3.metric("Итераций", len(result.iterations_data))

            # --- ТАБЛИЦА ИТЕРАЦИЙ ---
            st.subheader("Ход решения")
            # Превращаем данные в DataFrame для красивого вывода
            df = pd.DataFrame(
                result.iterations_data, 
                columns=["№", "x1", "x2", "Погрешность"]
            )
            # Отключаем индексацию pandas, так как у нас есть свой столбец №
            st.dataframe(df, use_container_width=True, hide_index=True)

            # --- ГРАФИК ---
            st.subheader("Визуализация системы")
            fig, ax = plt.subplots(figsize=(8, 6))
            
            r = result.solutions
            # Динамически подбираем масштаб вокруг корня
            x_vals = np.linspace(r[0]-2, r[0]+2, 100)
            y_vals = np.linspace(r[1]-2, r[1]+2, 100)
            X, Y = np.meshgrid(x_vals, y_vals)
            
            # Считаем неявные функции f(x,y) = 0
            Z1 = np.array([[sys_obj.funcs[0]([x, y]) for x in x_vals] for y in y_vals])
            Z2 = np.array([[sys_obj.funcs[1]([x, y]) for x in x_vals] for y in y_vals])
            
            # Рисуем линии, где функции равны нулю
            c1 = ax.contour(X, Y, Z1, levels=[0], colors='blue')
            c2 = ax.contour(X, Y, Z2, levels=[0], colors='green')
            
            # Добавляем легенду для контуров
            ax.clabel(c1, fmt={0: 'f1(x,y)=0'}, inline=True)
            ax.clabel(c2, fmt={0: 'f2(x,y)=0'}, inline=True)
            
            # Отмечаем найденный корень
            ax.scatter([r[0]], [r[1]], color='red', s=100, label="Найденный корень", zorder=5)
            
            ax.axhline(0, color='black', lw=0.5, alpha=0.5)
            ax.axvline(0, color='black', lw=0.5, alpha=0.5)
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend()
            
            st.pyplot(fig)
            
        else:
            st.error(f"Ошибка: {result.error_message}")