import bpy
import bmesh

# We cannot use folder relative file importation e.g.
#     from bmesh_utils import ...
# because the "blender --python [...]" does some tricks
import sys, os

sys.path.append(os.path.dirname(__file__))
from UI_utils import promote_bmesh_to_UI_object, UI_cleanup_default_scene
from bmesh_half_sphere import bmesh_of_half_icosphere

if __name__ == "__main__":
    ### Deal with the geometry (bmesh level)
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

    ### Deal with the UI
    UI_cleanup_default_scene()

    obj_half_sphere_facing_X_plus = promote_bmesh_to_UI_object(
        bmesh_half_sphere_facing_X_plus,
        "Half_Sphere_facing_X_plus",
    )
    bpy.context.collection.objects.link(obj_half_sphere_facing_X_plus)

    obj_half_sphere_facing_X_minus = promote_bmesh_to_UI_object(
        bmesh_half_sphere_facing_X_minus,
        "Half_Sphere_facing_X_minus",
    )
    bpy.context.collection.objects.link(obj_half_sphere_facing_X_minus)
