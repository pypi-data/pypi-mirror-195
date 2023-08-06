from maintenance import unstable, UnstableWarning
import pytest

def test_unstable() -> None:
    @unstable()
    def broken() -> int:
        return 42
    
    with pytest.warns(UnstableWarning):
        assert broken() == 42