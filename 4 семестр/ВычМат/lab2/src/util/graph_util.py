import numpy as np
import plotly.graph_objects as go

AXIS_STYLE = dict(
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.1)', # Почти прозрачная сетка (как засечки)

            showline=False,          # Скрываем внешнюю линию рамки
            zeroline=True,           # Включаем центральную ось
            zerolinecolor='black',   # Цвет центральной оси
            zerolinewidth=2,

            automargin=True,

            ticks="outside",
            tickcolor='black',
            tickwidth=1,
            ticklen=7,
            mirror=True,

            minor=dict(
                ticklen=3,
                tickwidth=1,
                tickcolor='black',
                ticks="outside",
            )
        )

def create_equation_plot(eq, a, b, root=None):
    """
    Создает интерактивный график для одного нелинейного уравнения.
    """
    margin = (b - a) * 0.2
    x_range = np.linspace(a - margin, b + margin, 500)
    y_range = [eq.f(x) for x in x_range]
    
    fig = go.Figure()
    
    # График функции
    fig.add_trace(go.Scatter(
        x=x_range, y=y_range, 
        mode='lines', 
        name=f"f(x) = {eq.func_str}", 
        line=dict(color='#1f77b4', width=2)
    ))
    
    fig.add_hline(y=0, line_width=1.5, line_color="black")
    fig.add_vline(x=0, line_width=1.5, line_color="black")
    
    # Закрашенный отрезок [a, b]
    fig.add_vrect(
        x0=a, x1=b, 
        fillcolor="gray", opacity=0.2, 
        layer="below", line_width=0, 
        name="Отрезок поиска"
    )
    
    # Точка корня
    if root is not None:
        fig.add_trace(go.Scatter(
            x=[root], y=[0], 
            mode='markers', 
            marker=dict(color='red', size=12, line=dict(color='DarkSlateGrey', width=2)), 
            name="Найденный корень"
        ))
    
    fig.update_layout(
        xaxis_title="x",
        yaxis_title="f(x)",
        hovermode="x unified",
        dragmode="zoom", # Включаем зум выделением
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black"),
        xaxis=AXIS_STYLE,
        yaxis=AXIS_STYLE
    )
    
    return fig


def create_system_plot(sys_obj, root_x, root_y):
    """
    Создает интерактивный график для системы нелинейных уравнений (линии уровня f(x,y)=0).
    """
    margin = 4
    x_vals = np.linspace(root_x - margin, root_x + margin, 400)
    y_vals = np.linspace(root_y - margin, root_y + margin, 400)
    
    # Считаем неявные функции f(x,y)
    Z1 = np.array([[sys_obj.funcs[0]([x, y]) for x in x_vals] for y in y_vals])
    Z2 = np.array([[sys_obj.funcs[1]([x, y]) for x in x_vals] for y in y_vals])
    
    fig = go.Figure()
    
    # Линия f1(x,y) = 0
    fig.add_trace(go.Contour(
        z=Z1, x=x_vals, y=y_vals,
        contours=dict(
            start=0, 
            end=0, 
            size=1,
            coloring='lines'
        ),
        line=dict(width=3, color='blue'), 
        colorscale=[[0, 'blue'], [1, 'blue']],
        showscale=False,
        name="f1(x,y)=0",
        hovertemplate='x: %{x:.4f}<br>y: %{y:.4f}<extra>f1=0</extra>'
    ))
    
    # Линия f2(x,y) = 0
    fig.add_trace(go.Contour(
        z=Z2, x=x_vals, y=y_vals,
        contours=dict(
            start=0, 
            end=0, 
            size=1,
            coloring='lines' 
        ),
        line=dict(width=3, color='green'),
        colorscale=[[0, 'green'], [1, 'green']],
        showscale=False,
        name="f2(x,y)=0",
        hovertemplate='x: %{x:.4f}<br>y: %{y:.4f}<extra>f2=0</extra>'
    ))
    
    # Точка корня
    fig.add_trace(go.Scatter(
        x=[root_x], y=[root_y], 
        mode='markers', 
        marker=dict(color='red', size=12, symbol='circle', line=dict(color='black', width=1)), 
        name="Найденный корень"
    ))
    
    # Оси
    fig.add_hline(y=0, line_width=1, line_color="black", opacity=0.5)
    fig.add_vline(x=0, line_width=1, line_color="black", opacity=0.5)
    
    fig.update_layout(
        hovermode='closest',
        xaxis_title="x1 (x)",
        yaxis_title="x2 (y)",
        dragmode="zoom",
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black"),

        xaxis=AXIS_STYLE,
        yaxis=AXIS_STYLE
    )
    
    return fig