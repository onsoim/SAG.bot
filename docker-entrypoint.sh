#!/bin/sh

tor >> log/$(date +"%Y-%m-%d")_tor.log &

# curl --socks5-hostname localhost:9050 ifconfig.me
while [ `netstat -ant | grep 9050 | wc -l` -eq 0 ]
do
    sleep 1
done

python3 -u src/__main__.py >> log/$(date +"%Y-%m-%d").log &

/bin/sh
