# Using the Blender based examples with docker 
<!-- TOC -->

- [Building the docker image](#building-the-docker-image)
  - [Building without cloning](#building-without-cloning)
  - [Building after cloning](#building-after-cloning)
- [Running things](#running-things)

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

In order to obtain the flags/options of TunNetGenCpp one can run
```bash
docker run --rm vcity/tunnetgenmodeller cylinder_example.py --help
```

In order to obtain the resulting PLY format files, you must provide the 
`outputdir` that matches the mounted volume e.g.

```bash
docker run --rm -v $(pwd)/data:/Output vcity/tunnetgenmodeller cylinder_example.py --subdivision 5 --outputdir /Output 
```

## Debugging teh container
If you want to check the container state, you can run
```bash
docker run --rm -it --entrypoint bash  vcity/tunnetmodeller
```
