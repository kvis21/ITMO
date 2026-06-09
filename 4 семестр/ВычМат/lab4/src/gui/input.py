# gui/input.py
import streamlit as st

def render_input_section():
    st.sidebar.header("Входные данные")
    
    input_type = st.sidebar.selectbox(
        "Выберите способ ввода данных:",
        ["Пример", "Ручной ввод", "Из файла"]
    )
    
    x_list, y_list = [], []
    
    if input_type == "Пример":
        h = 0.4
        x0 = 0
        n = 11
        f = lambda xi: 18 * xi / (xi ** 4 + 10)

        x_list = [round(x0 + i * h, 2) for i in range(n)]
        y_list = [round(f(x), 2) for x in x_list]
        st.sidebar.success("Загружен математический пример!")
        
    elif input_type == "Ручной ввод":
        st.sidebar.subheader("Ручной ввод координат")
        x_str = st.sidebar.text_input("Вектор X (через пробел):", "1.0 2.0 3.0 4.0 5.0")
        y_str = st.sidebar.text_input("Вектор Y (через пробел):", "2.1 3.9 6.2 8.0 10.3")
        try:
            x_list = [float(i.replace(',', '.')) for i in x_str.split()]
            y_list = [float(i.replace(',', '.')) for i in y_str.split()]
        except ValueError:
            st.sidebar.error("Ошибка! Проверьте корректность чисел.")
            return None, None, 0
            
    elif input_type == "Из файла":
        st.sidebar.subheader("Загрузка текстового файла")
        uploaded_file = st.sidebar.file_uploader("Выберите .txt файл (1 строка - X, 2 строка - Y)", type=["txt"])
        if uploaded_file is not None:
            try:
                lines = uploaded_file.read().decode("utf-8").splitlines()
                if len(lines) >= 2:
                    x_list = [float(i.replace(',', '.')) for i in lines[0].split()]
                    y_list = [float(i.replace(',', '.')) for i in lines[1].split()]
                else:
                    st.sidebar.error("В файле должно быть как минимум 2 строки.")
            except Exception as e:
                st.sidebar.error(f"Не удалось прочитать файл: {e}")
                return None, None, 0
        else:
            st.sidebar.info("Загрузите файл для начала расчета.")
            return None, None, 0

    n = len(x_list)
    if n == 0 or len(y_list) == 0:
        return None, None, 0
        
    if n != len(y_list):
        st.sidebar.error(f"Размеры не совпадают! X: {n}, Y: {len(y_list)}")
        return None, None, 0
        
    if n < 2:
        st.sidebar.error("Необходимо минимум 2 точки.")
        return None, None, 0

    st.sidebar.write("**Входная таблица:**")
    st.sidebar.dataframe({"X": x_list, "Y": y_list}, height=300)
    return x_list, y_list, n