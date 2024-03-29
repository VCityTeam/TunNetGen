import bpy
import bmesh
import bpyhelpers


######################## UI related
def duplicate_object(src_obj, data=True):
    ###
    # Note: failed to use
    # bpy.ops.object.duplicate_move()
    # as pointed out by
    # https://blender.stackexchange.com/questions/135597/how-to-duplicate-an-object-in-2-8-via-the-python-api
    # because the OBJECT_OT_duplicate argument (as well as
    # TRANSFORM_OT_translate) is
    # * neither documented in the reference API
    #   https://docs.blender.org/api/current/bpy.ops.object.html
    # * nor (apparently) to be found in the Python API sources (that seem
    #   to be held within the same repository as blender sources) that is
    #   https://projects.blender.org/blender/blender
    #
    # We thus fold back to the "under the hood" approach that is e.g. given by
    # * https://blender.stackexchange.com/questions/45099/duplicating-a-mesh-object
    # * https://b3d.interplanety.org/en/making-a-copy-of-an-object-using-the-blender-python-api/
    #
    # The duplicated object ends up as being the currently selected object
    obj_copy = src_obj.copy()
    if data:
        obj_copy.data = obj_copy.data.copy()
    return obj_copy


def get_mesh_boundary_edges(object):
    if not hasattr(object, "data"):
        return 0
    if not isinstance(object.data, bpy.types.Mesh):
        return 0
    # We need to "convert" the UI "Mesh" type to a bmesh type.
    b_mesh = bmesh.new()  # Create a temporary bmesh container instance
    b_mesh.from_mesh(object.data)
    edges = bpyhelpers.bmesh_get_boundary_edges(b_mesh)
    b_mesh.free()
    return edges
