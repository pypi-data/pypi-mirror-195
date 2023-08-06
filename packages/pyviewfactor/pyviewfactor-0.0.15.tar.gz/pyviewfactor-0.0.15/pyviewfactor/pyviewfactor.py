""" PVF main functions"""


# Imports
from numba import njit
import pyvista as pv
import pandas as pd
import scipy.integrate
import numpy as np


# Functions
def fc_unstruc2poly(mesh_unstruc):
    """Convenience conversion function from UnstructuredGrid to PolyData

    Parameters
    ----------
    * **mesh_unstruc** : *pyvista.UnstructuredGrid*

        > Unstructured Pyvista Grid.

    Returns
    -------
    * *pyvista.PolyData*

        > The same mesh converted to a surface pyvista.PolyData.

    Examples
    --------
    >>> import pyviewfactor as pvf
    >>> import pyvista as pv
    >>> sphere = pv.Sphere(radius=0.5, center=(0, 0, 0))
    >>> subset = sphere.extract_cells(10)
    >>> subsetPoly = fc_unstruc2poly(subset)
    >>> subsetPoly
    PolyData (0x1fdd9786040)
      N Cells:    1
      N Points:    3
      X Bounds:    -5.551e-17, 3.617e-02
      Y Bounds:    0.000e+00, 4.682e-02
      Z Bounds:    -5.000e-01, -4.971e-01
      N Arrays:    0

    """

    # Get the points and cells
    points = mesh_unstruc.points
    faces = mesh_unstruc.cells
    # Return the same geometry as a pv.PolyData mesh
    return pv.PolyData(points, faces)


def get_visibility(c1, c2, strict=False):
    """Facets visibility:

    A test to check if two facets can "see" each other, taking the normals 
    into consideration (no obstruction tests, only normals orientations).

    Parameters
    ----------
    * **c1** : *pyvista.PolyData*

        > PolyData facet (pyvista format).

    * **c2** : *pyvista.PolyData*

        > PolyData facet (pyvista format).

    * **strict** : *Bool*

        > If *True*, checks all the points are able to see each other 
          (considering the face normal) and then continue. If some points are
          "begind the other faces, it will return *False*,
        > Else, compute the centroids visibility, and might print a warning if
          some points are "behind".

    Returns
    -------
    * **bool**

        > True when the facets "see" each other, False else.

    Examples
    --------
    >>> import pyvista as pv
    >>> import pyviewfactor as pvf
    >>> tri1 = pv.Triangle([[0.0, 1.0, 1.0],[1.0, 1.0, 1.0],[1.0, 0.0, 1.0]])
    >>> tri2 = pv.Triangle([[1.0, 0.0, 0.0],[1.0, 1.0, 0.0],[0.0, 1.0, 0.0]])
    >>> pvf.get_visibility(tri1, tri2,strict=False)
    True
    """

    # Checking if every point of c1 in "in front" of c2 with the sign of the
    # triple product:
    for pt in c1.points:
        v = pt - c2.points[0]
        edge2a = c2.points[0] - c2.points[1]
        edge2b = c2.points[0] - c2.points[2]
        # "triple" product computation --> "v.(edge2a x edge2b)"
        det = v.dot(np.cross(edge2a, edge2b))
        if det < 0:
            if not strict:
                print(
                    "... ! ... PVF Warning : at least one point of cell is \"behind\" cell2\n")
            else:
                return False

    # Test on the normals orientations for the visibility:
    # Get cell centers
    center1 = c1.cell_centers().points
    center2 = c2.cell_centers().points
    # Get the vector between the cell centers
    v21 = center1-center2
    # Get cell normals
    n1 = c1.cell_normals
    n2 = c2.cell_normals
    # Compute the 2 scalar product
    pos_dot_prod = np.einsum('ij,ij->i', v21, n2)
    neg_dot_prod = np.einsum('ij,ij->i', v21, n1)
    # Return result of visibility test
    if (pos_dot_prod > 0 and neg_dot_prod < 0):
        return True
    return False


def get_visibility_raytrace(face1, face2, obstacle):
    """Raytrace between face1 and face2

    A test to check if there is an obstruction between two facets.

    Parameters
    ----------
    * **face1** : *pyvista.PolyData*

        > face1 to be checked for obstruction.

    * **face2** : *pyvista.PolyData*

        > face2 to be checked for obstruction.

    * **obstacle** : *pyvista.PolyData*

        > The mesh inbetween, composing the potential obstruction.

    Returns
    -------
    * *bool*

        > True if no obstruction, False else.

    Examples
    --------
    >>> import pyvista as pv
    >>> import pyviewfactor as pvf
    >>> tri1 = pv.Triangle([[0.0, 1.0, 1.0],[1.0, 1.0, 1.0],[1.0, 0.0, 1.0]])
    >>> tri2 = pv.Triangle([[1.0, 0.0, 0.0],[1.0, 1.0, 0.0],[0.0, 1.0, 0.0]])
    >>> obstacle = pv.Circle(radius=3.0)
    >>> obstacle.translate([0, 0, 0.5], inplace = True)
    >>> pvf.get_visibility_raytrace(tri2, tri1, obstacle)
    False

    """
    # Define line segment from one cell center to the other
    start = face1.cell_centers().points[0]
    stop = face2.cell_centers().points[0]
    # Perform ray trace along the line segment
    # points : location of the intersection
    # ind : indices if the intersection cells
    points, ind = obstacle.ray_trace(start, stop, first_point=False)
    # If considering a single cell
    # /!\ Ce n'est pas le bon test, il faut checker si les points de départ
    # et d'arrivé appartiennet à "obstacle" !
    # tester si le obstacle est un maillage ouvert ?
    # tester
    if obstacle.n_cells == 1:
        # The cells are not obstructed if the ray trace from cell 1 to cell2
        # does *not* intersect the "obstacle" mesh, >> ind is empty
        return True if ind.size == 0 else False
    # Il manque un cas de figure

    # Else, if face1 and face2 are contained in the obstacle mesh
    else:
        # The cells are obstructed if the ray trace from cell 1 to cell 2 hits
        # the "obstacle" more than 3 times (on cell 1, cell 2 and at least once
        # somewhere in between)
        # If the cells are not obstructed, len(ind) should be == 2
        return False if len(ind) > 2 else True


def get_visibility_MT(face1, face2, obstacle):
    """Triangle / Ray intersection based on the Möeller-Trumbore algorithm

    A test to check if there is an obstruction between two facets, basaed on
    Möller-Trumbore algorithm

    **To add**: a "strict" argument, to check not the centroids, but all points
    of face1 against all point of face2 given an obstacle.

    Parameters
    ----------
    * **face1** : *pyvista.PolyData*

        > face1 to be checked for obstruction. *A single PolyData face*

    * **face2** : *pyvista.PolyData*. *A single PolyData face*

        > face2 to be checked for obstruction.

    * **obstacle** : *pyvista.PolyData*. *A single PolyData face, or a entire 
        mesh *

        > The mesh inbetween, composing the potential obstruction 

    Returns
    -------
    * *bool*

        > True if no obstruction, False else.

    Examples
    --------
    >>> import pyvista as pv
    >>> import pyviewfactor as pvf
    >>> tri2 = pv.Triangle([[0.0, 1.0, 1.0],[1.0, 1.0, 1.0],[1.0, 0.0, 1.0]])
    >>> tri1 = pv.Triangle([[1.0, 0.0, 0.0],[1.0, 1.0, 0.0],[0.0, 1.0, 0.0]])
    >>> obstacle = pv.Circle(radius=3.0)
    >>> obstacle.translate([0, 0, 0.5], inplace = True)
    >>> pvf.get_visibility_MT(tri2, tri1, obstacle)
    False

    """

    # Defining ray origin and vector
    ray_orig = face1.cell_centers().points[0]
    ray_end = face2.cell_centers().points[0]
    ray_dir = ray_end - ray_orig
    if not obstacle.is_all_triangles():
        obstacle.triangulate(inplace=True)
    vis = []
    for idx in range(obstacle.n_cells):
        v1, v2, v3 = obstacle.cell_points(idx)
        eps = 0.000001
        edge1 = v2 - v1
        edge2 = v3 - v1
        pvec = np.cross(ray_dir, edge2)
        det = edge1.dot(pvec)
        if abs(det) < eps:
            vis.append(True)
            continue
        inv_det = 1. / det
        tvec = ray_orig - v1
        u = tvec.dot(pvec) * inv_det
        if u < 0. or u > 1.:
            vis.append(True)
            continue
        qvec = np.cross(tvec, edge1)
        v = ray_dir.dot(qvec) * inv_det
        if v < 0. or u + v > 1.:
            vis.append(True)
            continue
        t = edge2.dot(qvec) * inv_det
        if t < eps:
            vis.append(True)
            continue
        if t > np.dot(ray_dir, ray_dir):
            vis.append(True)
            continue
        vis.append(False)
    return True if all(vis) else False


def trunc(values, decs=0):
    """Return values with *decs* decimals. 

    A function to truncate decimals in floats.

    Parameters
    ----------
    * **values** : *float*, or *numpy.array* (floats)

        A float value with decimals, or a numpy.array of floats

    * **decs** : *int*, optional

        The number of decimals to keep. The default is 0.

    Returns
    -------
    * *float*

        > The same flaot truncated with *decs* decimals, or a the same
        numpy.array of floats truncated.

    Examples
    --------
    >>> import pyvista as pv
    >>> import pyviewfactor as pvf
    >>> a = 1.23456789
    >>> pvf.trunc(a,2)
    1.23
    >>> tri1 = pv.Triangle([[0.111111, 1.111111, 1.111111],
                        [1.222222, 1.222222, 1.222222],
                        [1.333333, 0.333333, 1.333333]])
    >>> trunc(tri1.points,2)
    pyvista_ndarray([[0.11, 1.11, 1.11],
                     [1.22, 1.22, 1.22],
                     [1.33, 0.33, 1.33]])

    """
    return np.trunc(values*10**decs)/(10**decs)


@njit  # numba's just in time compilation offers a x2 speedup
def integrand(x, y, norm_q_carree, norm_p_carree, scal_qpq,
              scal_qpp, scal_pq, norm_qp_carree):
    """
    Return the integrand for a pair of edges of two facets for the view factor
    computation.

    Used in the *compute_viewfactor* function. 

    """
    integrand_function = np.log(y**2*norm_q_carree
                                + x**2*norm_p_carree
                                - 2*y*scal_qpq
                                + 2*x*scal_qpp
                                - 2*x*y*scal_pq
                                + norm_qp_carree
                                )*scal_pq
    return integrand_function


def compute_viewfactor(cell_1, cell_2, epsilon=0.001):
    """
    View factor computation between cell1 and cell2

    Parameters
    ----------
    * **cell_1** : *pyvista.PolyData* facet

        > The first cell.

    * **cell_2** : *pyvista.PolyData* facet

        > The second cell.

    * **epsilon** : *float*

        * Desired precision, default = 0.001
        * It should *never* be higher than 1e-10, where the precision is close
          to numpy's intergation error.
        * A good practice is not to get higher than the number of digits
          defining your `points`.
        * A precision  of 1e-8 with points define with 5 digits, for example,
          will lead to a zero view factor.

    Returns
    -------
    * *float*

        > The view factor from **cell_2** to **cell_1**.

    Examples
    --------
    >>> import pyvista as pv
    >>> import pyviewfactor as pvf
    >>> tri1 = pv.Triangle([[0.0, 1.0, 1.0],[1.0, 1.0, 1.0],[1.0, 0.0, 1.0]])
    >>> tri2 = pv.Triangle([[1.0, 0.0, 0.0],[1.0, 1.0, 0.0],[0.0, 1.0, 0.0]])
    >>> pvf.compute_viewfactor(tri1, tri2)
    0.07665424316999997

    """
    # View factor initialization
    FF = 0
    # Cell 1 preparation
    cell_1_poly = cell_1
    cell_1 = cell_1.cast_to_unstructured_grid()
    # Getting the cell points
    cell_1_points = cell_1.cell_points(0)
    # Creating vectors describing the oriented edges
    cell_1_points_roll = np.roll(cell_1_points, -1, axis=0)
    # [Ai,Bi,Ci,...,Ni] -> [Bi, Ci,..., Ni,Ai]
    vect_dir_elts_1 = cell_1_points_roll - cell_1_points
    # [[Bi-Ai], [Ci-Bi],...,[Ni-Ai]]
    # Ther euse to be a truncature, for test purposes
    # cell_1_points = trunc(cell_1_points, decs=10)

    # Same for cell 2
    cell_2_poly = cell_2
    cell_2 = cell_2.cast_to_unstructured_grid()
    cell_2_points = cell_2.cell_points(0)
    cell_2_points_roll = np.roll(cell_2_points, -1, axis=0)
    vect_dir_elts_2 = cell_2_points_roll - cell_2_points
    #cell_2_points = trunc(cell_2_points, decs=10)
    # Creation of a matrix N by M, with N the number of points defining cell 1
    # and M the number of points defining cell 2
    n_cols = np.shape(cell_2_points)[0]
    n_rows = np.shape(cell_1_points)[0]
    # Getting the number of vertexes for eaach cell
    nb_sommets_1 = n_rows
    nb_sommets_2 = n_cols
    # Creation of an empty dataframe of size N by M
    mat_vectors = np.zeros((n_rows, n_cols))
    vectors = pd.DataFrame(mat_vectors, dtype=object)
    # Filling the dataframe
    for row in range(n_rows):
        # Getting the coordinates of the vectors starting from Vertex i from
        # cell 1 to each vertex j from cell 2
        coord_repeat = np.tile(cell_1_points[row], (nb_sommets_2, 1))
        vect_sommets_1_to_2 = cell_2_points - coord_repeat
        # Filling the "vectors" dataframe
        vectors.iloc[row] = list(vect_sommets_1_to_2)
    vect_sommets_extra = vectors
    vect_sommets_intra_1 = vect_dir_elts_1
    vect_sommets_intra_2 = vect_dir_elts_2
    # Constants calculations for the contour integral
    area = cell_2_poly.compute_cell_sizes(area=True)['Area']
    A_q = area[0]
    constante = 4*np.pi*A_q
    # Initialisation of the integration error, and the contribution of each
    # edge intergal to the overall one
    err = 0
    s_i = 0
    s_j = 0
    # Getting the number of shared vertexes
    arr_test = np.argwhere(
        (cell_2_points[:, None, :] == cell_1_points[:, :]).all(-1)
    )
    nbre_sommets_partages = np.shape(arr_test)[0]
    # If the 2 cells don't share any vertices, "regular" computation of the
    # integral
    if nbre_sommets_partages == 0:
        for n in range(nb_sommets_2):
            p_n_np1 = tuple(vect_sommets_intra_2[n, :])
            norm_p_carree = np.dot(p_n_np1, p_n_np1)
            for m in range(nb_sommets_1):
                q_m_mp1 = tuple(vect_sommets_intra_1[m, :])
                norm_q_carree = np.dot(q_m_mp1, q_m_mp1)
                qm_pn = vect_sommets_extra.loc[m, n]
                norm_qp_carree = np.dot(qm_pn, qm_pn)
                scal_qpq = np.dot(qm_pn, q_m_mp1)
                scal_qpp = np.dot(qm_pn, p_n_np1)
                scal_pq = np.dot(q_m_mp1, p_n_np1)
                s_j, err = scipy.integrate.dblquad(
                    integrand,
                    0, 1,
                    lambda x: 0, lambda x: 1,
                    args=(
                        norm_q_carree,
                        norm_p_carree,
                        scal_qpq,
                        scal_qpp,
                        scal_pq,
                        norm_qp_carree
                    )
                )
                s_i += round(s_j/constante, 11)
                err += err/(nb_sommets_1 + nb_sommets_2)
    else:
        # When the cells share one edge or more:
        # Apply a virtual displacement by epsilon, according to the
        # centroid vector
        centroid_vec = cell_2_poly.cell_centers().points \
            - cell_1_poly.cell_centers().points
        # Normalization
        centroid_vec = centroid_vec / np.sqrt(np.sum(centroid_vec**2))
        for sommet_j in cell_2_points[:, :]:
            sommet_j += np.dot(centroid_vec, epsilon)[0]
        # After the displacement, update the matrix with every vector from
        # cell 1 vertices to every vertiuces of cell 2
        for row in range(n_rows):
            # Getting the coordinates of the vectors starting from Vertex i
            # from cell 1 to each vertex j from cell 2, as previously
            coord_repeat = np.tile(cell_1_points[row], (n_cols, 1))
            vect_sommets_i_to_j = cell_2_points - coord_repeat
            vectors.iloc[row] = list(vect_sommets_i_to_j)
        # Then proceed to the regular integral computation
        for n in range(nb_sommets_2):
            p_n_np1 = tuple(vect_sommets_intra_2[n, :])
            norm_p_carree = np.dot(p_n_np1, p_n_np1)
            for m in range(nb_sommets_1):
                q_m_mp1 = tuple(vect_sommets_intra_1[m, :])
                norm_q_carree = np.dot(q_m_mp1, q_m_mp1)
                qm_pn = vect_sommets_extra.loc[m, n]
                norm_qp_carree = np.dot(qm_pn, qm_pn)
                scal_qpq = np.dot(qm_pn, q_m_mp1)
                scal_qpp = np.dot(qm_pn, p_n_np1)
                scal_pq = np.dot(q_m_mp1, p_n_np1)
                s_j, err = scipy.integrate.dblquad(
                    integrand,
                    0, 1,
                    lambda x: 0, lambda x: 1,
                    args=(
                        norm_q_carree,
                        norm_p_carree,
                        scal_qpq,
                        scal_qpp,
                        scal_pq,
                        norm_qp_carree)
                )
                s_i += round(s_j/constante, 11)
                err += err/(nb_sommets_1 + nb_sommets_2)
    if s_i > 0:
        FF = s_i
    return FF


""" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ End Of File ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """
