import pytest
import pyvista as pv
import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
sys.path.append('../pyviewfactor/')
# import scipy.integrate
from pyviewfactor import fc_unstruc2poly


def test_fc_unstruc2poly():
    sphere = pv.Sphere(radius=0.5, center=(0, 0, 0))
    subset = sphere.extract_cells(10)
    subsetPoly = fc_unstruc2poly(subset)
    assert type(subset) == pv.core.pointset.UnstructuredGrid
    assert type(subsetPoly) == pv.core.pointset.PolyData