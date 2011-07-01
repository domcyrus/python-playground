#!/bin/bash

NUM_CONNECTIONS=1000
PORT=11111
SLEEP=2

while getopts "c:p:s:" flag; do
  case "$flag" in
    c) NUM_CONNECTIONS=$OPTARG;;
    p) PORT=$OPTARG;;
    s) SLEEP=$OPTARG;;
  esac
done

function netcat() {
  (printf "GET it\r\n\r\n";sleep 1;printf "netcat number: $1") | nc 0 $PORT -w 2 -i $SLEEP || echo "can't connect $1" >> stress.log
}

echo "Number of connections: $NUM_CONNECTIONS"
echo "Port: $PORT"

for i in `seq 1 ${NUM_CONNECTIONS}`; do
  netcat $i &
done

sleep $SLEEP
sleep $SLEEP
echo done
