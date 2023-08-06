import pytest

import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
sys.path.append('../pyviewfactor/')
# import scipy.integrate
from pyviewfactor import trunc


def test_trunc():
    a = 1.23456789
    output = trunc(a,2)
    assert output == 1.23