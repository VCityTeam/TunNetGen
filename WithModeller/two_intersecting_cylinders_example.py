import os
import bpy
import bmesh
import bpyhelpers
import math
import mathutils
from bmesh_cylinder import cylinder
from argument_parser_helper import parse_arguments


def main():
    args = parse_arguments()
    bpyhelpers.UI_cleanup_default_scene()

    ### A first (slightly fat) cylinder with capped ends
    first_cylinder = cylinder(radius=args.radius * 1.1, length=args.length * 0.9)
    bmesh_first_cylinder = first_cylinder.bmesh_of_cylinder_with_taps(
        subdivisions=args.subdivision, centered=True
    )

    # Because UI_booleean_union() requires (UI) objects (as opposed to a simple
    # mesh):
    obj_first_cylinder = bpyhelpers.UI_promote_bmesh_to_UI_object(
        bmesh_first_cylinder, "FirstCylinder"
    )
    bpy.context.collection.objects.link(obj_first_cylinder)

    ### A second (sligthly thinner) cylinder that (partly) occupies the same
    # spatial position as the first one (so they do intersect)
    second_cylinder = cylinder(radius=args.radius * 0.9, length=args.length * 1.2)
    bmesh_second_cylinder = second_cylinder.bmesh_of_cylinder_with_taps(
        subdivisions=args.subdivision, centered=True
    )
    bmesh.ops.rotate(
        bmesh_second_cylinder,
        verts=bmesh_second_cylinder.verts,
        # cent=(0.0, 0.0, 0.0),
        # Make the axis imperfectly orthogonal to check for numerical
        # surprises.
        matrix=mathutils.Matrix.Rotation(math.radians(87.0), 4, "Z"),
    )

    # Again, this is required because UI_booleean_union() requires (UI)
    # objects as arguments (as opposed to simple meshes):
    obj_second_cylinder = bpyhelpers.UI_promote_bmesh_to_UI_object(
        bmesh_second_cylinder, "SecondCylinder"
    )
    bpy.context.collection.objects.link(obj_second_cylinder)

    ### Realize the boolean intersection
    bpyhelpers.UI_boolean_union(obj_first_cylinder, obj_second_cylinder)

    bmesh_result = bpyhelpers.UI_demote_UI_object_with_mesh_to_bmesh(obj_first_cylinder)

    bpyhelpers.bmesh_assert_genus_number_boundaries(
        bmesh_result,
        0,
        0,
        "The topology of the two intersecting cylinders is wrong.",
    )

    ## Promote the resulting mesh to an (UI) object for exporting and
    # also for a possible UI interaction (when present)
    obj_intersecting_cylinders = bpyhelpers.UI_promote_bmesh_to_UI_object(
        bmesh_result, "IntersectingCylinders"
    )
    bpy.context.collection.objects.link(obj_intersecting_cylinders)
    if not args.headless:
        # The Blender UI is present and we need to unregister the first cylinder
        # that no longer exists as an autonomous UI object
        bpy.context.collection.objects.unlink(obj_first_cylinder)

    ### The geometry is now build and we can write it to the resulting PLY files.
    # Start with writing the triangulation
    triangulation_filename = os.path.join(
        args.outputdir,
        "two_intersecting_cylinders_"
        + str(args.subdivision)
        + "_radius_"
        + str(args.radius)
        + "_length_"
        + str(args.length)
        + "_triangulation.ply",
    )
    # "bpy.ops" methods apply on the objects that are selected (and sometimes
    # additionnaly to active objects). We thus have to select the cylinder
    obj_intersecting_cylinders.select_set(True)

    bpy.ops.wm.ply_export(
        filepath=triangulation_filename,
        check_existing=True,
        forward_axis="Y",
        up_axis="Z",
        global_scale=1.0,
        apply_modifiers=False,
        export_selected_objects=True,
        export_uv=True,
        export_normals=True,
        export_colors="SRGB",
        export_triangulated_mesh=True,
        ascii_format=True,
        filter_glob="*.ply",
    )
    # Eventually write the point cloud version (of the triangulation):
    bpyhelpers.convert_ply_triangulation_to_point_cloud(
        triangulation_filename, args.verbose
    )


if __name__ == "__main__":
    main()
