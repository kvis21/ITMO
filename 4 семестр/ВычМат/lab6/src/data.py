from dataclasses import dataclass
from typing import Callable, List, Optional


@dataclass
class ODE:
    name: str
    f: Callable[[float, float], float]
    exact: Optional[Callable[[float], float]]
    x0: float
    y0: float
    xn: float
    h: float
    formula: str


@dataclass
class MethodResult:
    name: str
    x: List[float]
    y: List[float]
    status: str
    error: Optional[float] = None
    runge_error: Optional[float] = None


@dataclass
class SolverState:
    ode: ODE
    h: float
    eps: float
    results: List[MethodResult]
