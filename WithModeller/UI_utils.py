import bpy
import bmesh

# We cannot use folder relative file importation e.g.
#     from bmesh_utils import ...
# because the "blender --python [...]" does some tricks
import sys, os

#
sys.path.append(os.path.dirname(__file__))
from bmesh_utils import bmesh_of_half_icosphere, bmesh_get_boundary_edges


def promote_bmesh_to_UI_object(src_bmesh, name):
    # Not sure why the following transfer to a new mesh is really needed.
    # Maybe it is due to the latter arising of the bmesh module and the need
    # to keep it compatible with the UI way of things (?), refer to
    # https://blender.stackexchange.com/questions/134867/how-bpy-ops-mesh-differs-from-bmesh-ops
    mesh_result = bpy.data.meshes.new("Mesh")
    src_bmesh.to_mesh(mesh_result)
    src_bmesh.free()

    # Make it an object (which adds it to the scene (?))
    return bpy.data.objects.new(name, mesh_result)


if __name__ == "__main__":
    bmesh_half_sphere_facing_X_plus = bmesh_of_half_icosphere(
        radius=2.0, subdivisions=4, angle=90.0
    )
    bmesh_half_sphere_facing_X_minus = bmesh_of_half_icosphere(
        radius=2.0, subdivisions=4, angle=-90.0
    )
    bmesh.ops.translate(
        bmesh_half_sphere_facing_X_minus,
        verts=bmesh_half_sphere_facing_X_minus.verts,
        vec=(5.0, 0.0, 0.0),
    )
    print(
        len(bmesh_get_boundary_edges(bmesh_half_sphere_facing_X_minus)),
        len(bmesh_get_boundary_edges(bmesh_half_sphere_facing_X_plus)),
    )

    # bmesh.ops.bridge_loops(bmesh_half_sphere_facing_X_plus)

    ################ Dealing with the UI

    # Avoid showing the splash screen
    bpy.context.preferences.view.show_splash = False

    # Remove the defaul Cube from the original scene
    objs = bpy.data.objects
    objs.remove(objs["Cube"], do_unlink=True)

    ### Promote bmeshes to (UI) objects
    obj_half_sphere_facing_X_plus = promote_bmesh_to_UI_object(
        bmesh_half_sphere_facing_X_plus,
        "Half_Sphere_facing_X_plus",
    )

    obj_half_sphere_facing_X_minus = promote_bmesh_to_UI_object(
        bmesh_half_sphere_facing_X_minus,
        "Half_Sphere_facing_X_minus",
    )

    ### Display the objects
    bpy.context.collection.objects.link(obj_half_sphere_facing_X_minus)
    bpy.context.collection.objects.link(obj_half_sphere_facing_X_plus)
