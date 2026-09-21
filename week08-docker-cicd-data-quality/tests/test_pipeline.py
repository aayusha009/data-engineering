# pytest automatically finds any file named test_*.py and any function named test_*
from src.pipeline import add, subtract


def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(5, 3) == 2