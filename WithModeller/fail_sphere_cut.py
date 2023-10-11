import bmesh
import mathutils
import math
import bpy


def bmesh_get_boundary_edges(src_bmesh):
    return [ele for ele in src_bmesh.edges if ele.is_boundary]


if __name__ == "__main__":
    bmesh_half_sphere = bmesh.new()
    bmesh.ops.create_icosphere(
        bmesh_half_sphere,  # At this stage it is still the full sphere
        radius=2.0,
        subdivisions=2,
        matrix=mathutils.Matrix.Identity(4),
    )
    bmesh.ops.bisect_plane(
        bmesh_half_sphere,
        geom=bmesh_half_sphere.verts[:]
        + bmesh_half_sphere.edges[:]
        + bmesh_half_sphere.faces[:],
        dist=0,
        plane_co=(0.0, 0.0, 0.0),
        plane_no=(0.0, 0.0, 1.0),
        use_snap_center=False,
        clear_outer=True,
        clear_inner=False,
    )

    boundary_edges = [
        ele
        for ele in bmesh_half_sphere.edges
        if ele.is_boundary and ele.calc_length() < 0.01
    ]
    bmesh.ops.collapse(bmesh_half_sphere, edges=boundary_edges)
    boundary_edges = [
        ele for ele in bmesh_half_sphere.edges if ele.is_boundary
    ]
    print("On the UI, there seems to be 10 edges on the boundary.")
    print("Yet they are ", len(boundary_edges), " edges.")
    print("Why is this?")
    print("A clue: below are the respective lenghts of the boundary edges")
    for edge in boundary_edges:
        print(edge.calc_length())

    ################ Dealing with the UI
    # Clean up the default scene
    bpy.context.preferences.view.show_splash = False
    objs = bpy.data.objects
    objs.remove(objs["Cube"], do_unlink=True)

    # Display the half sphere
    mesh_half_sphere = bpy.data.meshes.new("Mesh")
    bmesh_half_sphere.to_mesh(mesh_half_sphere)
    bmesh_half_sphere.free()
    obj_half_sphere = bpy.data.objects.new("HalfSphere", mesh_half_sphere)
    bpy.context.collection.objects.link(obj_half_sphere)
