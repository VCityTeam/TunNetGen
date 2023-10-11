import bpy
import bmesh
import math


# We cannot use folder relative file importation e.g.
#     from bmesh_utils import ...
# because the "blender --python [...]" does some tricks
import sys, os

sys.path.append(os.path.dirname(__file__))
from bmesh_cylinder import bmesh_make_cylinder
from UI_utils import promote_bmesh_to_UI_object, UI_cleanup_default_scene


################ Dealing with the UI
if __name__ == "__main__":
    UI_cleanup_default_scene()

    bmesh_cylinder = bmesh_make_cylinder(50, 5)
    scene = bpy.context.scene
    object_cylinder = promote_bmesh_to_UI_object(bmesh_cylinder, "Cylinder")
    bpy.context.collection.objects.link(object_cylinder)
