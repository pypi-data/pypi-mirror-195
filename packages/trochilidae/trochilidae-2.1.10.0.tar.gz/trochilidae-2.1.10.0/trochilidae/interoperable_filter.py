from sys import version_info

__all__ = ["interoperable_filter"]

interoperable_filter = None

if version_info >= (3, 0):
    interoperable_filter = filter
else:
    from itertools import ifilter
    interoperable_filter = ifilter