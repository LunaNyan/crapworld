FROM python:3.12.6-slim-bookworm as base
ENV LC_ALL 'C.UTF-8'

WORKDIR /etc/garbageworld
COPY . ${WORKDIR}

RUN \
    apk add --update --no-cache curl py-pip
    pip install -r /etc/garbageworld/requirements.txt

EXPOSE 11111

COPY docker/docker-entrypoint.sh /docker-entrypoint.sh

USER ${USER_ID}
ENTRYPOINT ["/bin/sh", "/docker-entrypoint.sh"]
