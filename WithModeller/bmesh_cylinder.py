import bmesh
import math
import mathutils

# We cannot use folder relative file importation e.g.
#     from bmesh_utils import ...
# because the "blender --python [...]" does some tricks
import sys, os

sys.path.append(os.path.dirname(__file__))
from bmesh_half_sphere import bmesh_of_half_icosphere
from bmesh_utils import (
    bmesh_from_data,
    bmesh_triangulate_quad_faces,
    bmesh_join,
    bmesh_get_boundary_edges,
    bmesh_assert_genus_number_boundaries,
)


class cylinder:
    """
    A triangulated cylinder with its principal axis lying along the X.
    """

    # Portions of the following code where inspired by
    # https://sinestesia.co/blog/tutorials/python-tubes-cilinders/
    def __init__(self, radius, length, segments=None):
        self.radius = radius
        self.length = length
        self.segments = segments

    def __assert_segments_initialized(self):
        if self.segments:
            return
        print("cylinder::segments was not initialized. Exiting")
        sys.exit(1)

    def vertex_circle(self, z_pos):
        """
        Return a ring of vertices sitting in a circle in a X-Y plane located at
        the given position along the z axis
        """
        self.__assert_segments_initialized()
        verts = []

        for i in range(self.segments):
            angle = (math.pi * 2) * i / self.segments
            verts.append(
                (
                    self.radius * math.cos(angle),
                    self.radius * math.sin(angle),
                    z_pos,
                )
            )

        return verts

    def face(self, i, row):
        """Return a face on a cylinder"""
        self.__assert_segments_initialized()

        if i == self.segments - 1:
            ring_start = self.segments * row
            base = self.segments * (row + 1)

            return [
                (base - 1, ring_start, base),
                (base - 1, base, (base + self.segments) - 1),
            ]

        else:
            base = (self.segments * row) + i
            return [
                (base, base + 1, base + self.segments + 1),
                (base, base + self.segments + 1, base + self.segments),
            ]

    def get_bmesh_of_cylinder_along_X(self):
        """
        Return an open-ended cylinder that is not terminated with
        n-gon faces.
        """
        self.__assert_segments_initialized()
        length_of_circle_edge = math.pi * 2 * self.radius / self.segments
        # Estimated (because we take the perimeter of the circle for the adjacent
        # discretizing polygon) number of edges to compose the length:
        number_of_edges = math.ceil(self.length / length_of_circle_edge)
        number_of_rows = number_of_edges + 1

        data = {"verts": [], "edges": [], "faces": []}

        for row in range(number_of_rows):
            z_pos = self.length * row / number_of_edges
            data["verts"].extend(self.vertex_circle(z_pos))

        for i in range(self.segments):
            for row in range(0, number_of_rows - 1):
                data["faces"].extend(self.face(i, row))

        bmesh_cylinder = bmesh_from_data(data)
        bmesh.ops.rotate(
            bmesh_cylinder,
            verts=bmesh_cylinder.verts,
            matrix=mathutils.Matrix.Rotation(math.radians(90.0), 4, "Y"),
        )

        bmesh_assert_genus_number_boundaries(
            bmesh_cylinder, 0, 2, "Open-ended cylinder topology is wrong."
        )
        return bmesh_cylinder

    def bmesh_of_cylinder_with_taps(self, subdivisions, centered=True):
        """
        Builds a triangulated cylinder (with principal axis being the X axis)
        terminated (on both ends) by two half-spheres.
        Args:
            subdivisions (_type_): number of subdivisions of the half-spheres
                                   used to tap the cylinder's ends.
            centered (bool, optional): Whether the cylinder should be centered
            on the y axis or not. Defaults to True.

        Returns:
          bmesh: the constructed capped cylinder.
        """

        bmesh_X_plus_cap = bmesh_of_half_icosphere(
            radius=self.radius, subdivisions=subdivisions, angle=90.0
        )

        # The terminal half-spheres, used to tap the cylinder ends, need to
        # be set sligthly aside from the cylinder before "gluing" them with
        # the cylinder. This is because bmesh.ops.bridge_loops(), the "gluing"
        # algorithm, will add new faces to bridge/gap the half-spheres with
        # the cylinder. And we don't want those faces to be degenerated (having
        # a zero size along the z axis).
        self.segments = len(bmesh_get_boundary_edges(bmesh_X_plus_cap))
        length_before_cap = math.pi * 2 * self.radius / self.segments
        bmesh.ops.translate(
            bmesh_X_plus_cap,
            verts=bmesh_X_plus_cap.verts,
            vec=(-length_before_cap, 0.0, 0.0),
        )

        ### We can now build the cylinder per se. We couldn't do it before
        # because the number of segments of the cylinder must match the number
        # of edges of the half-sphere boundary component (that in turn depends
        # on the subdivisions parameter)
        bmesh_cylinder = self.get_bmesh_of_cylinder_along_X()

        ### Tap the first cylinder end (the one standing on X=0 plane)
        # Note that after joining AND before bridge_looping we still have two
        # (disconnected) components.
        bmesh_one_cap_cylinder = bmesh_join([bmesh_X_plus_cap, bmesh_cylinder])

        # The cylinder has two ends. We must designate the edges
        EPSILON = 0.1  # FIXME: should depend on subdivisions
        edges_to_bridge = [
            ele
            for ele in bmesh_one_cap_cylinder.edges
            if ele.is_boundary and ele.verts[0].co.x <= 0.1
        ]

        bridge = bmesh.ops.bridge_loops(
            bmesh_one_cap_cylinder, edges=edges_to_bridge
        )
        # The bridging algorithm creates quad faces that must be triangulated
        bmesh_triangulate_quad_faces(bmesh_one_cap_cylinder, bridge["faces"])
        del bridge

        bmesh_assert_genus_number_boundaries(
            bmesh_one_cap_cylinder,
            0,
            1,
            "The topology of the one side capped cylinder is wrong.",
        )

        ### Proceed with tapping the second cylinder end
        bmesh_X_minus_cap = bmesh_of_half_icosphere(
            radius=self.radius, subdivisions=subdivisions, angle=-90.0
        )
        bmesh.ops.translate(
            bmesh_X_minus_cap,
            verts=bmesh_X_minus_cap.verts,
            vec=(self.length + length_before_cap, 0.0, 0.0),
        )

        bmesh_capped_cylinder = bmesh_join(
            [bmesh_X_minus_cap, bmesh_one_cap_cylinder]
        )
        bridge = bmesh.ops.bridge_loops(
            bmesh_capped_cylinder,
            edges=bmesh_get_boundary_edges(bmesh_capped_cylinder),
        )
        # The bridging algorithm creates quad faces that must be triangulated
        bmesh_triangulate_quad_faces(bmesh_capped_cylinder, bridge["faces"])
        del bridge

        if centered:
            bmesh.ops.translate(
                bmesh_capped_cylinder,
                verts=bmesh_capped_cylinder.verts,
                vec=(-self.length / 2.0, 0.0, 0.0),
            )
        bmesh_assert_genus_number_boundaries(
            bmesh_capped_cylinder,
            0,
            0,
            "The topology of the both sides capped cylinder is wrong.",
        )

        return bmesh_capped_cylinder


######################## Design notes
# The first version was indeed creating a geometrical cylinder but its faces
# were cylinder long quadrangles, when we needed "nicely behaved" triangles.
#
# def fail_bmesh_of_cylinder_along_X(radius, half_length, segments):
#     bmesh_cylinder = bmesh.new()
#     bmesh.ops.create_cone(
#         bmesh_cylinder,
#         cap_ends=False,
#         cap_tris=False,
#         segments=segments,
#         radius1=radius,
#         radius2=radius,
#         depth=2 * half_length,
#     )
#     bmesh.ops.rotate(
#         bmesh_cylinder,
#         verts=bmesh_cylinder.verts,
#         # cent=(0.0, 0.0, 0.0),
#         matrix=mathutils.Matrix.Rotation(math.radians(90.0), 4, "Y"),
#     )

#     return bmesh_cylinder
