#!/bin/bash

./hz_run.sh
for port in $(seq 5701 5703); do
    echo "Waiting for hazelcast on $port..."
    while ! $(curl -s http://localhost:$port/hazelcast/health/ready > /dev/null); do
        sleep 1
    done
done

./run.sh

facade_port=8081

for i in {1..10}; do
    msg="msg-${i}"
    echo "POST $msg..."
    bash -x -c "curl -s -d "$msg" http://127.0.0.1:$facade_port/facade_service > /dev/null"
done

echo "GET result 1:"
bash -x -c "curl http://127.0.0.1:$facade_port/facade_service"
echo

echo "GET result 2:"
bash -x -c "curl http://127.0.0.1:$facade_port/facade_service"
echo

echo "GET result 3:"
bash -x -c "curl http://127.0.0.1:$facade_port/facade_service"
echo
