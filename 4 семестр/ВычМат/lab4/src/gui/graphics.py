import streamlit as st
import plotly.graph_objects as go
import math
from typing import List
from data import ApproximationResult

def render_plots(x_data: List[float], y_data: List[float], results: List[ApproximationResult], best_name: str):
    st.markdown("#### Интерактивные графики аппроксимирующих функций")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode='markers',
        name='Исходные точки',
        marker=dict(color='red', size=10, symbol='circle'),
        hovertemplate='<b>Исходная точка</b><br>X: %{x}<br>Y: %{y}<extra></extra>',
        zorder=10  
    ))
    
    x_min, x_max = min(x_data), max(x_data)
    margin = (x_max - x_min) * 0.1 if x_max != x_min else 1.0
    x_smooth = [x_min - margin + i * (x_max - x_min + 2 * margin) / 200 for i in range(201)]
    
    
    for res in results:
        if res.coefficients is None:
            continue
            
        name = res.name
        coefs = res.coefficients
        y_smooth = []
        
        try:
            if name == "Линейная":
                y_smooth = [coefs[0] * x + coefs[1] for x in x_smooth]
            elif name == "Полином 2-й степени":
                y_smooth = [coefs[0] * (x**2) + coefs[1] * x + coefs[2] for x in x_smooth]
            elif name == "Полином 3-й степени":
                y_smooth = [coefs[0] * (x**3) + coefs[1] * (x**2) + coefs[2] * x + coefs[3] for x in x_smooth]
            elif name == "Экспоненциальная":
                y_smooth = [coefs[0] * math.exp(coefs[1] * x) for x in x_smooth]
            elif name == "Логарифмическая":
                y_smooth = [coefs[0] * math.log(x) + coefs[1] if x > 0 else None for x in x_smooth]
            elif name == "Степенная":
                y_smooth = [coefs[0] * (x**coefs[1]) if x > 0 else None for x in x_smooth]
            
            is_best = (name == best_name)
            line_style = dict(
                width=2.5 if is_best else 1.5,
                dash='solid' if is_best else 'dash'
            )
            
            label_name = f"{name}" if is_best else name
            
            fig.add_trace(go.Scatter(
                x=x_smooth,
                y=y_smooth,
                mode='lines',
                name=f"{label_name} (δ={res.delta:.4f})",
                line=line_style,
                hovertemplate=f'<b>{name}</b><br>X: %{{x}}<br>Y: %{{y:.4f}}<extra></extra>'
            ))
            
        except Exception:
            pass

    # 3. Настройка осей, сетки и темы графика
    fig.update_layout(
        dragmode="pan",
        xaxis_title="X",
        yaxis_title="Y",
        hovermode="closest",
        margin=dict(l=40, r=40, t=20, b=40),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.5)" 
        ),
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)', fixedrange=False),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)', fixedrange=False),
        plot_bgcolor='rgba(0,0,0,0)', 
    )
    
    st.plotly_chart(fig, use_container_width=True)