from abc import ABC, abstractmethod
from typing import TypeAlias, Union

NestedMatrix: TypeAlias = list[Union[float, int, "NestedMatrix"]]

class AlgoBase(ABC):
    @abstractmethod
    def compute(mat: NestedMatrix) -> NestedMatrix:
        pass