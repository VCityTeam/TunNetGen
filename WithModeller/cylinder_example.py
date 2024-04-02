import os
import sys
import argparse
import bpy
import bmesh
import bpyhelpers
from bmesh_cylinder import cylinder


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="""
        Generate a triangulation file and the associated point cloud file
        out of the Blender programmatically defined capped cylinder.
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Toggle verbose printing"
    )
    parser.add_argument(
        "--subdivision",
        help="Number of subdivisions that should be applied:"
        " 1 for few triangles, for 6 expect a FIXME M resulting file",
        default=6,
        type=int,
    )
    parser.add_argument(
        "--radius",
        help="Radius of the cylinder",
        default=1.7,
        type=float,
    )
    parser.add_argument(
        "--length",
        help="Lenght of the cylinder (without the half-sphere caps)",
        default=5.5,
        type=float,
    )
    parser.add_argument(
        "--outputdir",
        help="Directory for resulting PLY files",
        default=".",
        type=str,
    )
    if "--" in sys.argv:
        # We probably are running this script in UI mode (that is with commands
        # like `blender --python this_script.py -- --subdivision 2`) and thanks
        # to this
        # https://blender.stackexchange.com/questions/6817/how-to-pass-command-line-arguments-to-a-blender-python-script
        # we know how to modify sys.argv in order to avoid interactions with
        # blender CLI arguments/options:
        argv = sys.argv[sys.argv.index("--") + 1 :]  # get all args after "--"
        args = parser.parse_args(argv)
        args.headless = False
    else:
        args = parser.parse_args()
        args.headless = True
    if args.verbose:
        parser.print_help()
        print("Parsed arguments: ")
        for arg in vars(args):
            print("   ", arg, ": ", getattr(args, arg))
    return args


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
    triangulation_filename = (
        "cylinder_"
        + str(args.subdivision)
        + "_radius_"
        + str(args.radius)
        + "_length_"
        + str(args.length)
        + "_triangulation.ply"
    )
    triangulation_filename = os.path.join(args.outputdir, triangulation_filename)

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
