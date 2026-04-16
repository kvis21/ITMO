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
        # Если данных нет (например, файл не загружен), очищаем старые результаты
        st.session_state.pop('sys_result', None)
        return

    sys_obj, x0, eps = data["system"], data["x0"], data["eps"]

    # --- КЛЮЧЕВОЙ МОМЕНТ: Сброс при смене системы ---
    # Создаем уникальный идентификатор текущего ввода
    current_input_id = f"{sys_obj.func_str}_{x0}_{eps}"
    
    # Если параметры изменились по сравнению с прошлым разом — удаляем результат
    if st.session_state.get('last_input_id') != current_input_id:
        st.session_state.pop('sys_result', None)
        st.session_state['last_input_id'] = current_input_id

    # Кнопка расчета
    if st.button("Решить СНЛАУ"):
        solver = MethodManager.get_method(MethodType.NEWTON)
        # Сохраняем результат в сессию
        st.session_state['sys_result'] = solver.solve(sys_obj, x0=x0, eps=eps)
        # Принудительно перезапускаем, чтобы блок отрисовки ниже увидел изменения
        st.rerun() 
        
    # Блок отрисовки
    if 'sys_result' in st.session_state:
        result = st.session_state['sys_result']
        
        if result.success:
            st.success("Решение найдено!")
            # ... твой код вывода (таблицы, значения x1, x2) ...
            
            # График
            fig, ax = plt.subplots()
            # Важно: используем чистый numpy только для создания сетки координат
            r = result.solutions
            x_vals = np.linspace(r[0]-2, r[0]+2, 100)
            y_vals = np.linspace(r[1]-2, r[1]+2, 100)
            X, Y = np.meshgrid(x_vals, y_vals)
            
            # Вычисляем значения функций для контуров
            Z1 = np.array([[sys_obj.funcs[0]([x, y]) for x in x_vals] for y in y_vals])
            Z2 = np.array([[sys_obj.funcs[1]([x, y]) for x in x_vals] for y in y_vals])
            
            ax.contour(X, Y, Z1, levels=[0], colors='blue')
            ax.contour(X, Y, Z2, levels=[0], colors='green')
            ax.scatter([r[0]], [r[1]], color='red', zorder=5)
            st.pyplot(fig)
        else:
            st.error(result.error_message)