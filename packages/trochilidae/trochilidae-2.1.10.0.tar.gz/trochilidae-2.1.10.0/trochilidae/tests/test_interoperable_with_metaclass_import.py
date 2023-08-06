import pytest

def test_interoperable_with_metaclass_import():
    try:
        from trochilidae.interoperable_with_metaclass import interoperable_with_metaclass_six
    except Exception as ex:
        pytest.fail("import six failed:{0}".format(ex))

    try:
        from trochilidae.interoperable_with_metaclass import interoperable_with_metaclass_future
    except Exception as ex:
        pytest.fail("import future failed:{0}".format(ex))