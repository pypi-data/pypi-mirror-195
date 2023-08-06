import pytest

def test_interoperable_map_import():
    try:
        from trochilidae.interoperable_map import interoperable_map
    except Exception as ex:
        pytest.fail("import failed:{0}".format(ex))