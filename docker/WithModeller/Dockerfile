FROM python:3.10-slim

RUN apt-get update
RUN apt-get install -y git

# Provide bpy python module hidden dependencies, that is solve all the 
# ImportError one gets when running
#      python -c "import bpy"
RUN apt-get install -y libxrender1                    # for libXrender.so.1
RUN apt-get install -y mesa-utils libgl1-mesa-glx     # for libXxf86vm.so.1
RUN apt-get install -y libxi6                         # for libXi.so.6
RUN apt-get install -y libxkbcommon-x11-0             # for libxkbcommon.so.0
RUN apt-get install -y libgomp1                       # for libgomp.so.1
RUN apt-get install -y libsm6                         # for libSM.so.6

RUN git clone https://github.com/VCityTeam/TunNetGen.git
WORKDIR TunNetGen/WithModeller

### Although recent versions of blender DO allow for the usage of Blender as a 
# Python Module (including in headless mode that is without prefixing the python
# interpreter with the blender command like in "blender --python <my_script.py")
# there is a lingering suffering around the various stages and strategies of 
# the installation process, refer e.g. to
# https://stackoverflow.com/questions/78110373/how-to-install-bpy-module-python-linux
# https://docs.blender.org/api/current/info_advanced_blender_as_bpy.html
# https://blender.stackexchange.com/questions/294913/how-to-install-blenderbpy-version-3-1-2
# https://stackoverflow.com/questions/63178840/cannot-install-package-bpy-using-pip#63377253
# 
# In addition, and not to mention, the original bpy repository is not that
# straightfoward to find (and no https://github.com/uhlik/bpy is not what you 
# might think at first).
# 
# Eventuall note that trying to fix a "pip3 install bpy==4.0.0" that triggers an 
#   "Ignored the following versions that require a different python 
#    version: 2.82.1 Requires-Python >=3.7, <3.8"
# error message with the pip "--ignore-requires-python" flag is of no help.
#
# The trick for succeeding with the "bpy" package installation boils down to 
# choosing a "good" combo version of the pip3.X/python3.Y couple. And what is
# meant by "good" is "that eventually works, for undocumented reasons, after 
# a long set of trial&error sessions". Caveat emptor.
#
# Notes: 
#  - couldn't get it to run for python:3.12-slim (your mileage may vary).
#  - notice that installer blender itself (apt-get install -y blender) is 
#    hopefully not necessary (because blender pulls lots of dependencies that
#    are besides useless because running Blender UI from a simple docker
#    container cannot be effective because the container cannot access the
#    graphic board drivers)
RUN pip3 install git+https://github.com/VCityTeam/bpyhelpers.git@master
RUN pip3 install bpy
RUN python --version
ENTRYPOINT [ "python" ]
