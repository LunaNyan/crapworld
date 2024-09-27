FROM python:3.12.6-alpine

ADD . /app
WORKDIR /app
COPY .git/ ./.git/

RUN pip install -r requirements.txt

EXPOSE 11111

CMD [ "python", "./y2k_server.py" ]
