import pytest

def test_interoperable_get_arg_spec():
    try:
        from trochilidae.interoperable_get_arg_spec import interoperable_get_arg_spec
    except Exception as ex:
        pytest.fail("import failed:{0}".format(ex))