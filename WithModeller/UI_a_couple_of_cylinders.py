import bpy
import bmesh
import bpyhelpers
import math
import mathutils
from bmesh_cylinder import cylinder


if __name__ == "__main__":
    bpyhelpers.UI_cleanup_default_scene()

    subdivisions = 3
    ### A lenghty (compared to the transverses) cylinder.
    radius = 1.5
    length = 70.0
    bmesh_base_cylinder = cylinder(
        radius=radius, length=length
    ).bmesh_of_cylinder_with_taps(subdivisions=subdivisions, centered=False)

    obj_base_cylinder = bpyhelpers.UI_promote_bmesh_to_UI_object(
        bmesh_base_cylinder, "BaseCylinder"
    )
    bpy.context.collection.objects.link(obj_base_cylinder)

    ### A succession of transversal cylinders that intersects the central
    # backbone one
    offset = 9.0
    radius = radius * 0.9
    length = length / 2.0
    for i_trans in range(7):
        bmesh_transverse_cylinder = cylinder(
            radius=radius, length=length
        ).bmesh_of_cylinder_with_taps(subdivisions=subdivisions, centered=True)

        bmesh.ops.rotate(
            bmesh_transverse_cylinder,
            verts=bmesh_transverse_cylinder.verts,
            # cent=(0.0, 0.0, 0.0),
            matrix=mathutils.Matrix.Rotation(math.radians(87.0), 4, "Z"),
        )
        bmesh.ops.translate(
            bmesh_transverse_cylinder,
            verts=bmesh_transverse_cylinder.verts,
            vec=(1.0 + i_trans * offset, 0.0, 0.0),
        )
        obj_transverse_cylinder = bpyhelpers.UI_promote_bmesh_to_UI_object(
            bmesh_transverse_cylinder, "Tranverse"
        )
        bpy.context.collection.objects.link(obj_transverse_cylinder)
        bpyhelpers.UI_boolean_union(obj_base_cylinder, obj_transverse_cylinder)

    bmesh_result = bpyhelpers.UI_demote_UI_object_with_mesh_to_bmesh(obj_base_cylinder)

    bpyhelpers.bmesh_assert_genus_number_boundaries(
        bmesh_result,
        0,
        0,
        "The topology of the many intersecting cylinders is wrong.",
    )
