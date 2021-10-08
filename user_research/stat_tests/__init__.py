from ..utils import AlgorithmRegister

algorithms = AlgorithmRegister()
__all__ = []


def export_to_all(defn):
    globals()[defn.__name__] = defn
    __all__.append(defn.__name__)
    return defn


from . import test1
from . import test2
from . import conf_interval
