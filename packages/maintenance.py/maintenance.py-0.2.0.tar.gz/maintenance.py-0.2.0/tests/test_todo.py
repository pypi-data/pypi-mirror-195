from maintenance import todo
import pytest

def test_call() -> None:
    with pytest.raises(NotImplementedError):
        todo()

def test_decorator() -> None:
    @todo
    def not_implemented():
        return
    
    with pytest.raises(NotImplementedError):
        not_implemented()
