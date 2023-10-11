import bmesh
import math

# We cannot use folder relative file importation e.g.
#     from bmesh_utils import ...
# because the "blender --python [...]" does some tricks
import sys, os

sys.path.append(os.path.dirname(__file__))
from bmesh_utils import bmesh_from_data


def vertex_circle(segments, z):
    """Return a ring of vertices"""
    verts = []

    for i in range(segments):
        angle = (math.pi * 2) * i / segments
        verts.append((math.cos(angle), math.sin(angle), z))

    return verts


def face(segments, i, row):
    """Return a face on a cylinder"""

    if i == segments - 1:
        ring_start = segments * row
        base = segments * (row + 1)

        return [
            (base - 1, ring_start, base),
            (base - 1, base, (base + segments) - 1),
        ]

    else:
        base = (segments * row) + i
        return [
            (base, base + 1, base + segments + 1),
            (base, base + segments + 1, base + segments),
        ]


def bmesh_make_cylinder(segments, rows):
    """Make a cylinder"""

    data = {"verts": [], "edges": [], "faces": []}

    for z in range(rows):
        data["verts"].extend(vertex_circle(segments, z))

    for i in range(segments):
        for row in range(0, rows - 1):
            data["faces"].extend(face(segments, i, row))

    bmesh_cylinder = bmesh_from_data(data)
    return bmesh_cylinder
