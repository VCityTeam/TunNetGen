import os
import bpy
import bmesh
import bpyhelpers
from bmesh_cylinder import cylinder
from argument_parser_helper import parse_arguments


def main():
    args = parse_arguments()

    bpyhelpers.UI_cleanup_default_scene()

    ### An open ended cylinder (only for display and not saved to PLY file)
    if not args.headless:  # The Blender UI is present
        open_cylinder = cylinder(radius=args.radius, length=args.length, segments=20)
        bmesh_open_cylinder = open_cylinder.get_bmesh_of_cylinder_along_X()
        object_open_cylinder = bpyhelpers.UI_promote_bmesh_to_UI_object(
            bmesh_open_cylinder, "OpenCylinder"
        )
        # Registering for access in UI
        bpy.context.collection.objects.link(object_open_cylinder)

    ### A cylinder with capped ends (half-spheres).
    capped_cylinder = cylinder(radius=args.radius, length=args.length)
    bmesh_capped_cylinder = capped_cylinder.bmesh_of_cylinder_with_taps(
        subdivisions=args.subdivision
    )
    bmesh.ops.translate(
        bmesh_capped_cylinder,
        verts=bmesh_capped_cylinder.verts,
        vec=(0.0, 2.5 * args.radius, 0.0),
    )
    # Assert the resulting topology is what was expected
    bpyhelpers.bmesh_assert_genus_number_boundaries(
        bmesh_capped_cylinder,
        0,
        0,
        "The topology of the cylinder is wrong.",
    )
    if args.verbose:
        bpyhelpers.bmesh_print_topological_characteristics(bmesh_capped_cylinder)

    obj_capped_cylinder = bpyhelpers.UI_promote_bmesh_to_UI_object(
        bmesh_capped_cylinder, "CappedCylinder"
    )
    # Registering for access in UI
    bpy.context.collection.objects.link(obj_capped_cylinder)

    ### Write the resulting PLY files: start with the triangulation
    triangulation_filename = os.path.join(
        args.outputdir,
        "cylinder_"
        + str(args.subdivision)
        + "_radius_"
        + str(args.radius)
        + "_length_"
        + str(args.length)
        + "_triangulation.ply",
    )

    # "bpy.ops" methods apply on the objects that are selected (and sometimes
    # additionnaly to active objects). We thus have to select the cylinder
    obj_capped_cylinder.select_set(True)

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
    # And end with writing the point cloud version of the triangulation
    bpyhelpers.convert_ply_triangulation_to_point_cloud(
        triangulation_filename, args.verbose
    )


if __name__ == "__main__":
    main()
