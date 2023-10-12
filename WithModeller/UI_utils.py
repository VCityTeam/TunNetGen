import bpy
import bmesh


def promote_bmesh_to_UI_object(src_bmesh: bmesh.types.BMesh, name):
    # Not sure why the following transfer to a new mesh is really needed.
    # Maybe it is due to the latter arising of the bmesh module and the need
    # to keep it compatible with the UI way of things (?), refer to
    # https://blender.stackexchange.com/questions/134867/how-bpy-ops-mesh-differs-from-bmesh-ops
    mesh_result = bpy.data.meshes.new("Mesh")
    src_bmesh.to_mesh(mesh_result)
    src_bmesh.free()

    # Make it an object (which adds it to the scene (?))
    return bpy.data.objects.new(name, mesh_result)


def UI_cleanup_default_scene():
    # Avoid showing the splash screen
    bpy.context.preferences.view.show_splash = False

    # Remove the defaul Cube from the original scene
    objs = bpy.data.objects
    objs.remove(objs["Cube"], do_unlink=True)
    objs.remove(objs["Camera"], do_unlink=True)
    objs.remove(objs["Light"], do_unlink=True)
