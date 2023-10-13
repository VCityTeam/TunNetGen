import bpy
import bmesh
import math
import mathutils


# We cannot use folder relative file importation e.g.
#     from bmesh_utils import ...
# because the "blender --python [...]" does some tricks
import sys, os

sys.path.append(os.path.dirname(__file__))
from bmesh_cylinder import cylinder
from bmesh_utils import bmesh_assert_genus_number_boundaries
from UI_utils import (
    promote_bmesh_to_UI_object,
    UI_cleanup_default_scene,
    UI_boolean_union,
    demote_UI_object_with_mesh_to_bmesh,
)


if __name__ == "__main__":
    UI_cleanup_default_scene()

    radius = 1.5
    length = 6.0

    ### A cylinder with capped ends (half-spheres).
    first_cylinder = cylinder(radius=radius * 1.1, length=length * 0.9)
    bmesh_first_cylinder = first_cylinder.bmesh_of_cylinder_with_taps(
        subdivisions=4, centered=True
    )

    obj_first_cylinder = promote_bmesh_to_UI_object(
        bmesh_first_cylinder, "FirstCylinder"
    )
    bpy.context.collection.objects.link(obj_first_cylinder)

    ### A second cylinder that intersects the first one
    second_cylinder = cylinder(radius=radius * 0.9, length=length * 1.2)
    bmesh_second_cylinder = second_cylinder.bmesh_of_cylinder_with_taps(
        subdivisions=5, centered=True
    )
    bmesh.ops.rotate(
        bmesh_second_cylinder,
        verts=bmesh_second_cylinder.verts,
        # cent=(0.0, 0.0, 0.0),
        matrix=mathutils.Matrix.Rotation(math.radians(87.0), 4, "Z"),
    )

    obj_second_cylinder = promote_bmesh_to_UI_object(
        bmesh_second_cylinder, "SecondCylinder"
    )
    bpy.context.collection.objects.link(obj_second_cylinder)

    ### Boolean intersection
    UI_boolean_union(obj_first_cylinder, obj_second_cylinder)

    bmesh_result = demote_UI_object_with_mesh_to_bmesh(obj_first_cylinder)

    bmesh_assert_genus_number_boundaries(
        bmesh_result,
        0,
        0,
        "The topology of the two cylinders intersection is wrong.",
    )
