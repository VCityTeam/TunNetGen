
# Python API of Blender (bpy) generated geometries

<!-- TOC -->

- [Installation](#installation)
- [Interacting with the resulting geometries](#interacting-with-the-resulting-geometries)
- [Running things](#running-things)
- [Blender tricks](#blender-tricks)
- [References](#references)
- [Modeling notes](#modeling-notes)
- [Issues](#issues)
  - [Why is it required for PYTHONPATH to point to the virtual environnement](#why-is-it-required-for-pythonpath-to-point-to-the-virtual-environnement)

<!-- /TOC -->

## Installation

```bash
python3.10 -m venv venv
source venv/bin/activate
(venv) pip install -r requirements.txt
```

Then running a script is the traditional invocation e.g.

```bash
(venv) python cylinder_example.py -v --subdivision 5
```

## Interacting with the resulting geometries

If you wish to interact with the resulting geometries with the help of the
blender UI (that is use commands of the form `blender --python <some_script.py>`),
and because of 
[this issue](#why-is-it-required-for-pythonpath-to-point-to-the-virtual-environnement),
you will further need to define the following `PYTHONPATH` environnement 
variable

```bash
(venv) export PYTHONPATH=`pwd`:`pwd`/venv/lib/python3.10/site-packages
```

Using Blender UI with the constructed is achieved with e.g (**mind the 
additional " -- " argument**)

```bash
blender --python cylinder_example.py -- -v --subdivision 4
```

## Running things

```bash
blender --python UI_half_sphere.py
```
<img src="Pictures/Two_half_spheres.png" alt="Blender Python Two Half Sphere" width="500"/>

```bash
blender --python UI_cylinder.py 
```
<img src="Pictures/Cylinder_and_both_ended_capped_cylinder.png" alt="Blender Python Two Cylinders" width="500"/>

```bash
blender --python UI_two_intersecting_cylinders.py 
```
should yield something like

<img src="Pictures/Two_Intersecting_Cylinders.png" alt="Blender Python Two Cylinders" width="800"/>

Additionally
```bash
blender --python UI_a_couple_of_cylinders.py  
```
should yield something like
<img src="Pictures/Many_Intersecting_Cylinders.png" alt="Blender Python Many Cylinders" width="800"/> 

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

## Issues

### Why is it required for PYTHONPATH to point to the virtual environnement

The reasons for having to define the `PYTHONPATH` environnement variable are
probably [hinted/documented in this blender stackexchange thread](https://blender.stackexchange.com/questions/181928/does-blender-use-a-python-virtual-environment). 
The difficulty can be simply illustrated with the following set of commands

```bash
(venv) export PYTHONPATH='pure junk'     # Just making sure it is not set
(venv) python -c "import bpyhelpers"     # OK
(venv) echo "import bpyhelpers" > script.py
(venv) blender --python script.py        # FAILS with
  [...]
  File "<somepath>/script.py", line 1, in <module>
    import bpyhelpers
  ModuleNotFoundError: No module named 'bpyhelpers'
```

