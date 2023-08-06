from sys import version_info

__all__ = ["interoperable_map"]

interoperable_map = None

if version_info >= (3, 0):
    interoperable_map = map
else:
    from itertools import imap
    interoperable_map = imap