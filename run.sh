#!/bin/bash

services=(facade logging logging logging messages)
screens=(facade logging-1 logging-2 logging-3 messages)
start_port=8081
for ((i=0; i<${#services[@]}; i++)); do
    screen_name=${screens[i]}
    name=${services[i]}
    port=$((i+start_port))
    if ! $(screen -list | grep $screen_name > /dev/null); then
        echo "Starting $screen_name ($name) on port $port..."
        screen -S $screen_name -d -m python3 -m uvicorn $name-service.controller:app --reload --port $port
    fi
done

sleep 2
