from sys import version_info

__all__ = ["interoperable_reduce"]

interoperable_reduce = None

if version_info >= (3, 3):
    from functools import reduce
    interoperable_reduce = reduce
else:
    interoperable_reduce = reduce