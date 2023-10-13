import sys
import bmesh
import mathutils
import math

# We cannot use folder relative file importation e.g.
#     from bmesh_utils import ...
# because the "blender --python [...]" does some tricks
import sys, os

sys.path.append(os.path.dirname(__file__))
from bmesh_utils import (
    bmesh_assert_genus_number_boundaries,
    bmesh_get_boundary_edges,
)


def bmesh_of_half_icosphere(radius, subdivisions, angle):
    """_summary_

    Args:
        radius (_type_): radius of the original sphere (refer to
                        bmesh.ops.create_icosphere() documentation)
        subdivisions (_type_): refer to bmesh.ops.create_icosphere() documentation
        angle (_type_): angle in degrees with which to rotate the resulting bmesh

    Returns:
        _type_: the bmesh of a half sphere (properly oriented)
    """
    #

    # First note that for subdivisions=1 the equator goes through faces, as
    # opposed to higher values of subdivisions for which the equator is made
    # of a succession of vertices and edges.
    if subdivisions < 2:
        print("Subdivisions should be at least 2. Exiting")
        sys.exit(1)

    ###  Notes concerning the "topological" length of the half sphere boundary.
    # By "topological length" we mean the number of edges (as opposed to the
    # geometric length) of the resulting half sphere boundary which can be
    # obtained (refer below) with
    #    print("# boundary edges", len(get_bmesh_boundary_edges(bmesh_result)))
    # This topological length (of the resulting boundary) is a function of the
    # subdivisions argument that goes
    #     topo_length = 10 * 2 ** (subdivisions - 2)
    # Alas if we observe that "topological" length of bisected icosphere (as
    # build below) we (originaly) obtain the following table:
    # |--------------|-------------------|
    # | Subdivisions |  Number of Edges  |
    # |--------------|-------------------|
    # |      2       |    20  WRONG      |
    # |      3       |    50  WRONG      |
    # |      4       |    92  WRONG      |
    # |      5       |   172  WRONG      |
    # |     ...      |  ALLWAYS WRONG    |
    # |______________|___________________|
    #
    # The reasons for this failures comes from the fact that, depending on input
    # parameters, the "bmesh.ops.bisect_plane()" algorithm produces degenerated
    # edges of zero (or almost zero) length.
    # We thus need to weed out the boundary edges from the denegerated ones
    # (e.g. by collapsing "tiny" boundary edges), refer below for details.
    # Alas, as allways when dealing with un-exact geometry (algorithms), the
    # result is still partially wrong and
    #
    # | Subdivisions |  Number of Edges  |
    # |--------------|-------------------|
    # |      2       |         10  OK    |
    # |      3       |         20  OK    |
    # |      4       |         40  OK    |
    # |      5       |         80  OK    |
    # |      6       |        161 WRONG  |
    # |      7       |        320  OK    |
    # |      8       |        640  OK    |
    # |     ...      |        ... ???    |
    # |______________|___________________|

    bmesh_result = bmesh.new()
    bmesh.ops.create_icosphere(
        bmesh_result,  # At this stage it is still the full sphere
        radius=radius,
        subdivisions=subdivisions,
        matrix=mathutils.Matrix.Identity(4),
    )
    bmesh.ops.bisect_plane(
        bmesh_result,
        geom=bmesh_result.verts[:]
        + bmesh_result.edges[:]
        + bmesh_result.faces[:],
        dist=0,
        plane_co=(0.0, 0.0, 0.0),
        plane_no=(0.0, 0.0, 1.0),
        use_snap_center=False,
        clear_outer=True,
        clear_inner=False,
    )
    # Remove degenerated edges. For this we need to define some (always empiric
    # and arbitrary) threshold criteria.
    expected_boundary_edge_count = 10 * 2 ** (subdivisions - 2)

    expected_boundary_edge_length = (
        2 * math.pi * radius / expected_boundary_edge_count
    )
    edge_length_threshold = expected_boundary_edge_length / 2.0

    degenerated_boundary_edges = [
        ele
        for ele in bmesh_result.edges
        if ele.is_boundary and ele.calc_length() < edge_length_threshold
    ]
    bmesh.ops.collapse(bmesh_result, edges=degenerated_boundary_edges)

    # rotate the half sphere so that the "antenna faces" the X axis
    bmesh.ops.rotate(
        bmesh_result,
        verts=bmesh_result.verts,
        # cent=(0.0, 0.0, 0.0),
        matrix=mathutils.Matrix.Rotation(math.radians(angle), 4, "Y"),
    )

    # Check that the correction was efficient:
    resulting_boundary_edge_count = len(bmesh_get_boundary_edges(bmesh_result))
    if expected_boundary_edge_count != resulting_boundary_edge_count:
        print(
            "Warning: wrong number of resulting boundary edge count: ",
            "expected",
            expected_boundary_edge_count,
            "but got",
            resulting_boundary_edge_count,
        )

    bmesh_assert_genus_number_boundaries(
        bmesh_result, 0, 1, "Half-sphere topology is wrong."
    )

    return bmesh_result
