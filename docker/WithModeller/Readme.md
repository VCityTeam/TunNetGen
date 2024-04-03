# Using the Blender based examples with docker 
<!-- TOC -->

- [Building the docker image](#building-the-docker-image)
  - [Building without cloning](#building-without-cloning)
  - [Building after cloning](#building-after-cloning)
- [Running things](#running-things)
- [A short list of working examples](#a-short-list-of-working-examples)
- [Debugging the container](#debugging-the-container)

<!-- /TOC -->

## Building the docker image

### Building without cloning

```bash
docker build -t vcity/tunnetgenmodeller https://github.com/VCityTeam/TunNetGen.git -f docker/WithModeller/Dockerfile
```

### Building after cloning

From the root folder of the project
```bash
git clone https://github.com/VCityTeam/TunNetGen.git
cd TunNetGen
docker build -t vcity/tunnetgenmodeller -f docker/PureCPP/Dockerfile .
```

## Running things

In order to obtain the flags/options of e.g. the cylinder example one can run

```bash
docker run --rm vcity/tunnetgenmodeller cylinder_example.py --help
```

In order to obtain the resulting PLY format files, you must provide an the 
`--outputdir` flag with an argument that matches the mounted volume e.g.

```bash
docker run --rm -v $(pwd)/data:/Output vcity/tunnetgenmodeller cylinder_example.py --subdivision 5 --outputdir /Output 
```

that should create a `data/` directory within the invocation directory with
the expected `PLY` format files.

## A short list of working examples

```bash
docker run --rm -v $(pwd)/data:/Output vcity/tunnetgenmodeller cylinder_example.py --outputdir /Output --radius 0.4 --length 2.0 --subdivision 5
docker run --rm -v $(pwd)/data:/Output vcity/tunnetgenmodeller two_intersecting_cylinders_example.py --outputdir /Output --radius 0.75 --length 6.0 --subdivision 6
```

## Debugging the container
If you want to check the container state, you can run
```bash
docker run --rm -it --entrypoint bash  vcity/tunnetmodeller
```
