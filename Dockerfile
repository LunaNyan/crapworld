FROM python:3.12.10-alpine3.21

ADD . /app
WORKDIR /app
COPY .git/ ./.git/

RUN pip install -r requirements.txt
RUN apk add git

EXPOSE 11111

CMD [ "python", "./y2k_server.py" ]

LABEL org.opencontainers.image.source https://github.com/lunanyan/crapworld