#~/bin/bash

if ! $(screen -list | grep "consul-dev" > /dev/null); then
    screen -S "consul-dev" -d -m consul agent -dev
fi
