import bmesh


def bmesh_from_data(data):
    # We should be very suspicious about this dependency of bmesh
    # towards the UI (bpy module)
    import bpy

    """Create a bmesh out of data"""

    mesh = bpy.data.meshes.new("dummy_name_that_will_be_trashed")
    mesh.from_pydata(data["verts"], data["edges"], data["faces"])
    bmesh_result = bmesh.new()
    bmesh_result.from_mesh(mesh)
    del mesh

    return bmesh_result


def bmesh_duplicate(src_bmesh):
    # A bmesh is just a python object, refer e.g. to
    # https://blender.stackexchange.com/questions/90724/what-is-the-best-way-to-copy-append-geometry-from-one-bmesh-to-another
    return src_bmesh.copy()


def bmesh_get_boundary_edges(src_bmesh):
    return [ele for ele in src_bmesh.edges if ele.is_boundary]


def bmesh_join(list_of_bmeshes, normal_update=False):
    # This is copy of zeffi's answer found at
    # https://blender.stackexchange.com/questions/50160/scripting-low-level-join-meshes-elements-hopefully-with-bmesh/50186#50186
    """takes as input a list of bm references and outputs a single merged bmesh
    allows an additional 'normal_update=True' to force _normal_ calculations.
    """

    bm = bmesh.new()
    add_vert = bm.verts.new
    add_face = bm.faces.new
    add_edge = bm.edges.new

    for bm_to_add in list_of_bmeshes:
        offset = len(bm.verts)

        for v in bm_to_add.verts:
            add_vert(v.co)

        bm.verts.index_update()
        bm.verts.ensure_lookup_table()

        if bm_to_add.faces:
            for face in bm_to_add.faces:
                add_face(tuple(bm.verts[i.index + offset] for i in face.verts))
            bm.faces.index_update()

        if bm_to_add.edges:
            for edge in bm_to_add.edges:
                edge_seq = tuple(
                    bm.verts[i.index + offset] for i in edge.verts
                )
                try:
                    add_edge(edge_seq)
                except ValueError:
                    # edge exists!
                    pass
            bm.edges.index_update()

    if normal_update:
        bm.normal_update()

    return bm
