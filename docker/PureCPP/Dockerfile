FROM alpine:3.16
LABEL maintainer "VCityTeam"

RUN apk add --no-cache g++
RUN apk add --no-cache make
RUN apk add --no-cache cmake

COPY PureCPP TunNetGenCpp

WORKDIR TunNetGenCpp
RUN mkdir build
RUN cmake -B build 
RUN make -j -C build

ENTRYPOINT ["./build/tunNetGen"]
CMD ["-o","output/pc.xyz"]