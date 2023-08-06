from maintenance import deprecated
import pytest

def test_deprecated() -> None:
    @deprecated()
    def old(a):
        return a
    
    with pytest.deprecated_call():
        assert old(42) == 42