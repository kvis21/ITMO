from abc import ABC, abstractmethod
import math
from typing import Callable

from src.data import Function, Callback, Result

class Method(ABC):
    def __init__(self, k):
        self.k = k

    def runge_rule(self, i_prev, i_curr, eps):
        return abs(i_curr - i_prev) / (2**self.k-1) <= eps

    def solve(self, **kwargs) -> Callback:
        func_obj, a, b, eps = self._get_params(kwargs)
        f = func_obj.function

        if not self.check_convergence(func_obj, a, b):
            return Callback(error="Интеграл не существует")

        sigma = eps / 1000 
        intervals = self.get_intervals(func_obj, a, b, sigma)
        
        try:
            n_total = 4
            max_iter = 20
            
            portions = [max(2, int(n_total * (end - start) / (b - a))) for start, end in intervals]

            def get_sum(current_portions):
                res = 0.0
                for (start, end), portion in zip(intervals, current_portions):
                    res += self._calculate_integral(f, start, end, portion)
                return res

            i_prev = get_sum(portions)
            for _ in range(max_iter):
                portions = [p * 2 for p in portions]
                n_total *= 2
                
                i_curr = get_sum(portions)
                
                if self.runge_rule(i_prev, i_curr, eps):
                    return Callback(result=Result(i_curr, n_total))
                i_prev = i_curr

            return Callback(result=Result(i_curr, n_total), error="Точность не достигнута")
            
        except (ValueError, ZeroDivisionError, OverflowError):
            return Callback(error="Интеграл не существует")
    

    @abstractmethod
    def _calculate_integral(self, f: Callable, a: float, b: float, n: int) -> float:
        pass


class BaseIntegrationMethod:
    def _check_value(self, y: float):
        if math.isinf(y) or math.isnan(y):
            raise ValueError("функция имеет разрыв.")

    def _get_params(self, kwargs):
        return kwargs.get('function'), kwargs.get('a'), kwargs.get('b'), kwargs.get('eps')
    
    def _is_antisymmetric_around(self, func_obj: Function, p: float, a: float, b: float) -> bool:
        """
        Проверяет, является ли функция кососимметричной (антисимметричной) 
        относительно точки разрыва p на максимальном симметричном радиусе.
        """
        R = min(p - a, b - p)
        if R <= 1e-12:
            return False  
        
        f = func_obj.function
        test_steps = [0.001, 0.01, 0.1, 0.5, 0.9]
        for step in test_steps:
            dx = R * step
            try:
                y_left = f(p - dx)
                y_right = f(p + dx)
                
                if math.isnan(y_left) or math.isnan(y_right) or math.isinf(y_left) or math.isinf(y_right):
                    continue
                
                if abs(y_left + y_right) > 1e-5:
                    return False
            except Exception:
                return False
        return True

    def check_convergence(self, func_obj: Function, a: float, b: float) -> bool:
        """Проверяет сходимость несобственного интеграла 2 рода с учетом главного значения Коши."""
        for i, pt in enumerate(func_obj.singular_points):
            if a <= pt <= b:
                if func_obj.p_orders[i] >= 1.0:
                    if not self._is_antisymmetric_around(func_obj, pt, a, b):
                        return False
        return True

    def get_intervals(self, func_obj: Function, a: float, b: float, sigma: float):
        """Разбивает отрезок на подмножества, исключая окрестности точек разрыва и зануляя симметричные участки."""
        
        effective_intervals = [(a, b)]
        
        for i, p in enumerate(func_obj.singular_points):
            if a <= p <= b and func_obj.p_orders[i] >= 1.0:
                if self._is_antisymmetric_around(func_obj, p, a, b):
                    R = min(p - a, b - p)
                    new_intervals = []
                    for start, end in effective_intervals:
                        if start < p - R:
                            new_intervals.append((start, min(end, p - R)))
                        if end > p + R:
                            new_intervals.append((max(start, p + R), end))
                    effective_intervals = new_intervals

        final_intervals = []
        for start, end in effective_intervals:
            if start >= end:
                continue
            
            active_singularities = sorted([p for p in func_obj.singular_points if start <= p <= end])
            intervals = []
            curr_a = start
            
            for p in active_singularities:
                if abs(p - start) < 1e-12:
                    curr_a = start + sigma
                elif start < p < end:
                    intervals.append((curr_a, p - sigma))
                    curr_a = p + sigma
                elif abs(p - end) < 1e-12:
                    intervals.append((curr_a, end - sigma))
                    curr_a = end
                    break
                    
            if curr_a < end:
                intervals.append((curr_a, end))
                
            final_intervals.extend(intervals)

        return [i for i in final_intervals if i[0] < i[1]]