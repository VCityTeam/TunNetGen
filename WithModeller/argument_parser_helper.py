import sys
import argparse


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
