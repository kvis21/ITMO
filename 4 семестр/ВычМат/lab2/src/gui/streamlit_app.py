import streamlit as st
from equation import EQUATIONS, SYSTEMS
from gui.equation_ui import render_equation_page
from gui.system_ui import render_system_page

def run_app():
    st.sidebar.title("Навигация")
    page = st.sidebar.radio("Выберите раздел:", ["Уравнение", "Система"])

    if page == "Уравнение":
        render_equation_page(EQUATIONS)
    else:
        render_system_page(SYSTEMS)