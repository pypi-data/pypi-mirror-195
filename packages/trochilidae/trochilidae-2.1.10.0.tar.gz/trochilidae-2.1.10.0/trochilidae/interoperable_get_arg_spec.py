import inspect
from sys import version_info

__all__ = ["interoperable_get_arg_spec"]

interoperable_get_arg_spec = None

if version_info[0] >= 3:
    interoperable_get_arg_spec = inspect.getfullargspec
else:
    interoperable_get_arg_spec = inspect.getargspec