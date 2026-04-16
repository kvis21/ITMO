from methods.base import MethodType, Method
from methods.newton import NewtonMethod
from methods.simple_iteration import SimpleIterationMethod
from methods.chord import ChordMethod
from methods.secant import SecantMethod


class MethodManager:
    @staticmethod
    def get_method(method_type: MethodType) -> Method:
        mapping = {
            MethodType.NEWTON: NewtonMethod(),
            MethodType.SIMPLE_ITERATION: SimpleIterationMethod(),
            MethodType.CHORD: ChordMethod(),
            MethodType.SECANT: SecantMethod(),
        }
        return mapping.get(method_type)