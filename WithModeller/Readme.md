
# Python API of Blender (bpy) generated geometries

## Running things

```bash
blender --python UI_half_sphere.py
blender --python UI_cylinder.py 
```

## Blender tricks
* [Increase vertices to a cylinder](https://blender.stackexchange.com/questions/193384/i-want-to-increase-the-number-of-vertices-in-a-cylinder)
* [Deleting faces](https://www.youtube.com/watch?v=At23FTDEu7E): select the face and use the `x` key
* [Selecting the edge loops](https://docs.blender.org/manual/en/2.79/modeling/meshes/selecting/edges_faces.html) (that is edges on the boundary of a surface)

* Showing the [number of selected primitives](https://blender.stackexchange.com/questions/145032/the-number-of-objects-selected) (vertices, edges, faces):
 go in the 3D Viewport to the top right under Viewport Overlays (icon is an open circle intersecting a closed circle) and enable the Statistics checkbox.

## References
* [bmesh module operations documentation](https://docs.blender.org/api/current/bmesh.ops.html)
* [Exporting bmesh to PLY](https://blenderartists.org/t/mesh-to-point-cloud/1124144/29)
* [edge/face loops using python](https://blenderartists.org/t/how-do-i-work-with-edge-face-loops-using-python/1228205/2)
* [Bmesh structure design](https://wiki.blender.org/wiki/Source/Modeling/BMesh/Design#Connectivity_Cycles)
* [Shaping Models With BMesh](https://behreajj.medium.com/shaping-models-with-bmesh-in-blender-2-9-2f4fcc889bf0)

## Modeling notes


