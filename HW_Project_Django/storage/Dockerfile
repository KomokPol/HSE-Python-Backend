FROM postgres:14-alpine
LABEL maintainer="KomokPol"

ARG USER_NAME
ARG USER_PASSWORD

ENV POSTGRES_PASSWORD=KomokPol
ENV POSTGRES_USER=KomokPol
ENV POSTGRES_DB=posts

RUN apk add --no-cache tzdata
EXPOSE 5432
ENV TZ=Europe/London