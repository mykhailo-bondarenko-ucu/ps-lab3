#!/bin/bash

services=(facade logging logging logging messages messages)
screens=(facade logging-1 logging-2 logging-3 messages-1 messages-2)
start_port=8081
for ((i=0; i<${#services[@]}; i++)); do
    screen_name=${screens[i]}
    name=${services[i]}
    port=$((i+start_port))
    if ! $(screen -list | grep $screen_name > /dev/null); then
        echo "Starting $screen_name ($name) on port $port..."
        echo logfile screenlogs/$screen_name.screenlog > screenlogs/$screen_name-config
        screen -L -c screenlogs/$screen_name-config -S $screen_name -d -m python3 -m pkg.$name-service.controller --port $port
    fi
done

sleep 5
