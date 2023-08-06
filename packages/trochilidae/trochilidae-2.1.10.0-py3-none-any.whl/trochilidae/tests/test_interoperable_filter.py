import pytest

def test_interoperable_filter_import():
    try:
        from trochilidae.interoperable_filter import interoperable_filter
    except Exception as ex:
        pytest.fail("import failed:{0}".format(ex))