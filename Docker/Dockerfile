FROM python:3.10-alpine

RUN apk --no-cache add bash gcc make musl-dev openjdk11-jdk maven \
    && wget https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein -O /usr/local/bin/lein \
    && chmod +x /usr/local/bin/lein \
    && lein

COPY ./programs /programs
COPY ./web-app /web-app

WORKDIR /programs
RUN chmod +x compile.sh \
    && ./compile.sh

WORKDIR /web-app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

EXPOSE 8080
ENTRYPOINT ["python3"]
CMD ["-u","app.py"]
