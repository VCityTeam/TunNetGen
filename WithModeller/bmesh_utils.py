import sys
import bmesh
import mathutils
import math


def bmesh_duplicate(src_bmesh):
    # A bmesh is just a python object, refer e.g. to
    # https://blender.stackexchange.com/questions/90724/what-is-the-best-way-to-copy-append-geometry-from-one-bmesh-to-another
    return src_bmesh.copy()


def bmesh_get_boundary_edges(src_bmesh):
    return [ele for ele in src_bmesh.edges if ele.is_boundary]


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
    # Notes concerning the "topological" length (the number of edges as
    # opposed to the geometric length) of the resulting boundary in function
    # of the subdivisions argument.
    #
    # Obtaining that length can be done with e.g.
    #    print("# boundary edges", len(get_bmesh_boundary_edges(lower_half)))
    #
    # Note that for subdivisions=1 the equator goes through faces, as opposed
    # to higher values of subdivisions for which the equator is made of a
    # succession of vertices and edges.
    #
    # The correspondance table goes:
    #
    # |   Subdivisions   |           Number of Edges              |
    # |------------------|----------------------------------------|
    # |        2         |    20   Warning: refer to above note   |
    # |        3         |    50   (  20*2 + 10 =  ( 20 +  5)*2)  |
    # |        4         |    92   (  50*2 -  8 =  ( 50 -  4)*2)  |
    # |        5         |   172   (  92*2 - 12 =  ( 92 -  6)*2)  |
    # |        6         |   336   ( 172*2 -  8 =  (172 -  4)*2)  |
    # |        7         |   650   ( 336*2 - 22 =  (336 - 11)*2)  |
    # |        8         |  1296   ( 650*2 -  4 =  (650 -  2)*2)  |
    # |        9         |  2592   (               1296      *2)  |
    # |       10         |  5216   (2592*2 + 32 = (2592 + 16)*2)  |
    # |       11         | 10546   (5216*2 +114 = (5216 + 57)*2)  |
    # |__________________|________________________________________|

    if subdivisions < 2:
        print("Subdivisions should be at least 2. Exiting")
        sys.exit(1)
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
    # rotate the half sphere so that the "antenna faces" the X axis
    bmesh.ops.rotate(
        bmesh_result,
        verts=bmesh_result.verts,
        # cent=(0.0, 0.0, 0.0),
        matrix=mathutils.Matrix.Rotation(math.radians(angle), 4, "Y"),
    )

    return bmesh_result
