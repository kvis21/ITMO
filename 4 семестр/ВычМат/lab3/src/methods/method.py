from abc import ABC, abstractmethod
import math

class Method(ABC):
    @abstractmethod
    def solve(self, *args, **kwargs): pass
    
class BaseIntegrationMethod:
    def _check_value(self, y: float):
        if math.isinf(y) or math.isnan(y):
            raise ValueError("функция имеет разрыв.")

    def _get_params(self, kwargs):
        return kwargs.get('function'), kwargs.get('a'), kwargs.get('b'), kwargs.get('eps')