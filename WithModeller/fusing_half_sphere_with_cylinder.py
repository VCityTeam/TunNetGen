import bpy
import bmesh

# We cannot use folder relative file importation e.g.
#     from bmesh_utils import ...
# because the "blender --python [...]" does some tricks
import sys, os

sys.path.append(os.path.dirname(__file__))
from UI_utils import promote_bmesh_to_UI_object, UI_cleanup_default_scene
from bmesh_utils import bmesh_join, bmesh_get_boundary_edges
from bmesh_half_sphere import (
    bmesh_of_half_icosphere,
    bmesh_of_cylinder_along_X,
)


# At some point normal harmonization will be required....
#
# def recalculate_normals(mesh):
#     """Make normals consistent for mesh"""

#     bm = bmesh.new()
#     bm.from_mesh(mesh)

#     bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

#     bm.to_mesh(mesh)
#     bm.free()


if __name__ == "__main__":
    radius = 2.0
    half_cylinder_length = 0.3
    subdivisions = 4
    bmesh_half_sphere_facing_X_plus = bmesh_of_half_icosphere(
        radius=radius, subdivisions=subdivisions, angle=90.0
    )
    bmesh_half_sphere_facing_X_minus = bmesh_of_half_icosphere(
        radius=radius, subdivisions=subdivisions, angle=-90.0
    )
    bmesh.ops.translate(
        bmesh_half_sphere_facing_X_minus,
        verts=bmesh_half_sphere_facing_X_minus.verts,
        vec=(2 * half_cylinder_length, 0.0, 0.0),
    )

    segments = len(bmesh_get_boundary_edges(bmesh_half_sphere_facing_X_minus))
    if segments != len(
        bmesh_get_boundary_edges(bmesh_half_sphere_facing_X_plus)
    ):
        print("Two half-spheres have a different number of segments.")
        print("Facing X minus", segments)
        print(
            "Facing X plus",
            len(bmesh_get_boundary_edges(bmesh_half_sphere_facing_X_plus)),
        )
        print("Exiting")
        sys.exit(1)

    print("Segments: ", segments)

    bmesh_cylinder = bmesh_of_cylinder_along_X(
        radius=radius,
        half_length=half_cylinder_length,
        segments=segments,
    )
    junko = bmesh_join([bmesh_half_sphere_facing_X_minus, bmesh_cylinder])
    bmesh.ops.bridge_loops(junko, edges=bmesh_get_boundary_edges(junko))

    ################ Dealing with the UI
    UI_cleanup_default_scene()

    obj_half_sphere_facing_X_minus = promote_bmesh_to_UI_object(
        junko,
        "Half_Sphere_facing_X_plus",
    )
    bpy.context.collection.objects.link(obj_half_sphere_facing_X_minus)

    ### Promote bmeshes to (UI) objects
    # obj_half_sphere_facing_X_plus = promote_bmesh_to_UI_object(
    #     bmesh_half_sphere_facing_X_plus,
    #     "Half_Sphere_facing_X_plus",
    # )
    # bpy.context.collection.objects.link(obj_half_sphere_facing_X_plus)

    # obj_half_sphere_facing_X_minus = promote_bmesh_to_UI_object(
    #     bmesh_half_sphere_facing_X_minus,
    #     "Half_Sphere_facing_X_minus",
    # )
    # bpy.context.collection.objects.link(obj_half_sphere_facing_X_minus)
