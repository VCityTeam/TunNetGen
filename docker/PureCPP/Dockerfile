FROM alpine:3.16
LABEL maintainer "VCityTeam"

RUN apk add --no-cache g++
RUN apk add --no-cache cmake
WORKDIR PureCPP
RUN mkdir build
WORKDIR build
RUN cmake ..
RUN make

CMD ["./tunNetGen"]
