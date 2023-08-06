from future.utils import with_metaclass as with_metaclass_future
from six import with_metaclass as with_metaclass_six

__all__ = ["interoperable_with_metaclass_future", "interoperable_with_metaclass_six"]


def interoperable_with_metaclass(with_metaclass, metaclass):
    return type("{0}Wrapper".format(metaclass.__name__), (with_metaclass(metaclass),), {})


def interoperable_with_metaclass_future(metaclass):
    return interoperable_with_metaclass(with_metaclass_future, metaclass)


def interoperable_with_metaclass_six(metaclass):
    return interoperable_with_metaclass(with_metaclass_six, metaclass)
