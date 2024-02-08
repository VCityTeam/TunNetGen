# Docker for the the CPP version 


## Building

### Building without cloning
```bash
docker build -t vcity/tunnetgencpp https://github.com/VCityTeam/TunNetGen.git -f docker/PureCPP/Dockerfile
```

### Building after cloning

From the root folder of the project
```bash
docker build -t vcity/tunnetgencpp -f docker/PureCPP/Dockerfile .
```

## Running

In order to obtain the flags/options of TunNetGenCpp one can run
```bash
docker run --rm vcity/tunnetgencpp:latest --help
```

To create the pointcloud pc.xyz in a data folder at the root of the project run
```bash
docker run --rm -v $(pwd)/data:/TunNetGenCpp/output vcity/tunnetgencpp:latest
```

You can override the path to the created project with 
```bash
docker run --rm -v $(pwd)/data:/TunNetGenCpp/output vcity/tunnetgencpp:latest -o output/pc.xyz 
```

If you want to check the container state, you can run
```bash
docker run --rm -it -v $(pwd)/data:/TunNetGenCpp/output vcity/tunnetgencpp:latest sh
```
