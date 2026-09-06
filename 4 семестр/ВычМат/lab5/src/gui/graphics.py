# gui/graphics.py
from typing import Callable, List, Optional

import plotly.graph_objects as go

import methods
from data import InterpolationResult

COLORS = {
    "Лагранж": "blue",
    "Ньютон (конечные разности)": "yellow",
    "Ньютон (разделенные разности)": "green",
    "Гаусс": "orange",
    "Стирлинг": "purple",
    "Бессель": "brown",
}


def _eval_on_grid(func: Callable, x_list: List[float], y_list: List[float],
                  grid: List[float]) -> List[Optional[float]]:
    """Вычисляет значения интерполяционного многочлена на сетке точек."""
    values = []
    for xv in grid:
        res = func(xv, x_list, y_list)
        values.append(res.value if res.value is not None else None)
    return values


def _add_curve(fig, func: Callable, x_list, y_list, grid, name: str):
    values = _eval_on_grid(func, x_list, y_list, grid)
    if None not in values:
        fig.add_trace(go.Scatter(
            x=grid, y=values, mode="lines", name=name,
            line=dict(color=COLORS.get(name, "gray"), width=2),
        ))


def render_plots(x_list: List[float], y_list: List[float],
                 results: List[InterpolationResult], x_point: float) -> go.Figure:
    """Строит график узлов интерполяции, интерполяционных многочленов и точки интерполяции."""
    x0, x1 = min(x_list), max(x_list)
    span = max(x1 - x0, 1e-12)
    grid = [x0 + i * span / 250 for i in range(251)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_list, y=y_list, mode="markers",
        name="Узлы интерполяции",
        marker=dict(size=9, color="red"),
    ))

    _add_curve(fig, methods.lagrange_interpolation, x_list, y_list, grid, "Лагранж")
    _add_curve(fig, methods.newton_finite, x_list, y_list, grid, "Ньютон (конечные разности)")
    _add_curve(fig, methods.newton_divided, x_list, y_list, grid, "Ньютон (разделенные разности)")
    _add_curve(fig, methods.gauss_first, x_list, y_list, grid, "Гаусс (1-ая формула)")
    _add_curve(fig, methods.gauss_second, x_list, y_list, grid, "Гаусс (2-ая формула)")
    _add_curve(fig, methods.stirling, x_list, y_list, grid, "Стирлинг")
    _add_curve(fig, methods.bessel, x_list, y_list, grid, "Бессель")

    point_value = next((r.value for r in results if r.name == "Многочлен Лагранжа"), None)
    if point_value is not None:
        fig.add_trace(go.Scatter(
            x=[x_point], y=[point_value], mode="markers",
            name=f"Точка x = {x_point}",
            marker=dict(size=12, color="magenta", symbol="star"),
        ))

    fig.update_layout(
        xaxis_title="x",
        yaxis_title="y",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        height=500,
    )
    return fig
