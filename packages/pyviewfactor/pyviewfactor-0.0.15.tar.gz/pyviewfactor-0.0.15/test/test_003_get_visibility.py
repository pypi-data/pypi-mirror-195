import pytest
import pyvista as pv
import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
sys.path.append('../pyviewfactor/')
# import scipy.integrate
from pyviewfactor import get_visibility


def test_get_visibility():
    tri1 = pv.Triangle([[0.0, 1.0, 1.0],[1.0, 1.0, 1.0],[1.0, 0.0, 1.0]])
    tri2 = pv.Triangle([[1.0, 0.0, 0.0],[1.0, 1.0, 0.0],[0.0, 1.0, 0.0]])
    assert get_visibility(tri1, tri2) == True
    tri1 = pv.Triangle([[1.0, 0.0, 1.0],[1.0, 1.0, 1.0],[0.0, 1.0, 1.0]])
    tri2 = pv.Triangle([[1.0, 0.0, 0.0],[1.0, 1.0, 0.0],[0.0, 1.0, 0.0]])
    assert get_visibility(tri1, tri2) == False