from typing import Callable, List, Optional

import plotly.graph_objects as go


COLORS = {
    "Метод Эйлера": "blue",
    "Рунге-Кутта 4": "green",
    "Милн": "orange",
    "Точное решение": "red",
}


def render_plots(x_exact: List[float], y_exact: List[Optional[float]],
                 results: list, ode_name: str) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_exact, y=y_exact, mode="lines",
        name="Точное решение",
        line=dict(color="red", width=3, dash="dash"),
    ))

    for r in results:
        fig.add_trace(go.Scatter(
            x=r.x, y=r.y, mode="lines+markers",
            name=r.name,
            line=dict(color=COLORS.get(r.name, "gray"), width=2),
            marker=dict(size=4),
        ))

    fig.update_layout(
        title=f"Решение ОДУ: {ode_name}",
        xaxis_title="x",
        yaxis_title="y",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        height=500,
    )
    return fig
