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

echo "GET result:"
bash -x -c "curl http://127.0.0.1:$facade_port/facade_service"
echo

echo "Press enter to start turning off"
read

stop_ports=(8082 8083)
for i in $(seq 0 $((${#stop_ports[@]} - 1)) ); do
    stop_port=${stop_ports[i]}
    pid=$(lsof -i :$stop_port | awk '{print $2}' | head -n 2 | tail -n 1)
    echo "Sending SIGINT to localhost:$stop_port (${pid})..."
    kill ${pid}
    echo "Shut down a hazelcast member and press enter..."
    read
    echo "GET result:"
    bash -x -c "curl http://127.0.0.1:$facade_port/facade_service"
    echo
done

