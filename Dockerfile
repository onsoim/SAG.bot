
FROM alpine

LABEL maintainer="onsoim <onsoim@gmail.com>" 

RUN apk upgrade --no-cache

RUN apk add --no-cache \
    gcc \
    g++ \
    cmd:pip3 \
    python3-dev

RUN apk add --no-cache \
    tor

RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    echo "Asia/Seoul" > /etc/timezone

RUN rm -rf \
    /var/cache/* \
    /root/.cache/*

WORKDIR /Bot

COPY requirements.txt .

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "/Bot/docker-entrypoint.sh" ]

# docker build --no-cache -t sag.bot:0.1 .
# docker run --rm -it -v $(pwd):/Bot sag.bot:0.1 /bin/sh

# docker save sag.bot:0.1 -o sag.bot_v0.1.tar.gz
