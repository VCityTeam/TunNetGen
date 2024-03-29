import bpy
import bmesh
import bpyhelpers
from bmesh_cylinder import cylinder


if __name__ == "__main__":
    bpyhelpers.UI_cleanup_default_scene()

    ### An open ended cylinder
    radius = 1.5
    length = 6.0
    open_cylinder = cylinder(radius=radius * 0.9, length=length * 1.1, segments=20)
    bmesh_open_cylinder = open_cylinder.get_bmesh_of_cylinder_along_X()
    object_open_cylinder = bpyhelpers.UI_promote_bmesh_to_UI_object(
        bmesh_open_cylinder, "OpenCylinder"
    )
    bpy.context.collection.objects.link(object_open_cylinder)

    ### A cylinder with capped ends (half-spheres).
    capped_cylinder = cylinder(radius=radius * 1.1, length=length * 0.9)
    bmesh_capped_cylinder = capped_cylinder.bmesh_of_cylinder_with_taps(subdivisions=6)
    bmesh.ops.translate(
        bmesh_capped_cylinder,
        verts=bmesh_capped_cylinder.verts,
        vec=(0.0, 2.5 * radius, 0.0),
    )
    obj_capped_cylinder = bpyhelpers.UI_promote_bmesh_to_UI_object(
        bmesh_capped_cylinder, "CappedCylinder"
    )
    bpy.context.collection.objects.link(obj_capped_cylinder)
