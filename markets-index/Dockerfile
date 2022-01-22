FROM mozilla/sbt AS builder
USER root
ARG TAG=0.14.0-M1
WORKDIR /builder
ADD https://github.com/ergolabs/ergo-dex-backend/archive/refs/tags/$TAG.tar.gz .
RUN tar zxvf $TAG.tar.gz && mv ergo-dex-backend-$TAG/* .
RUN export SBT_OPTS="-Xmx2G -XX:+UseConcMarkSweepGC -XX:+CMSClassUnloadingEnabled -Xss2M  -Duser.timezone=GMT" && \
    sbt markets-index/assembly && \
    mv ./modules/markets-index/target/scala-*/MarketsIndex-assembly-*.jar ./markets-index.jar

FROM adoptopenjdk:11-jre
WORKDIR /app
COPY --from=builder /builder/markets-index.jar .
COPY application.conf .
CMD ["java","-jar","markets-index.jar","application.conf"]