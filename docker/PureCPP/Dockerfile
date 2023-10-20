FROM alpine:3.16
LABEL maintainer "VCityTeam"

RUN apk add --no-cache g++
RUN apk add --no-cache make
RUN apk add --no-cache cmake

COPY PureCPP PureCPP

WORKDIR PureCPP
RUN mkdir build
RUN cmake -B build 
RUN make -C build

CMD [".build/tunNetGen"]