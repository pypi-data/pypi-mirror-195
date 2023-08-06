import pytest

def test_interoperable_reduce_import():
    try:
        from trochilidae.interoperable_reduce import interoperable_reduce
    except Exception as ex:
        pytest.fail("import failed:{0}".format(ex))