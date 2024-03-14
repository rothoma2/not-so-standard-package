import pytest
import sys

# import features

sys.path.append('/home/arlindo/not-so-standard-package')
from features.utils import gl4_converter


@pytest.fixture
def test__gl4_converter___input_1():
    return 'dlflgglg'


@pytest.fixture
def test__gl4_converter___output_1():
    return 'LLLLLLLL'


@pytest.fixture
def test__gl4_converter___input_2():
    return 'dL4lGG@!'


@pytest.fixture
def test__gl4_converter___output_2():
    return 'LUDLUUSS'


def test_gl4_converter__test_1(test__gl4_converter___input_1,test__gl4_converter___output_1):
    s =gl4_converter(test__gl4_converter___input_1)
    print(s)
    assert s == test__gl4_converter___output_1