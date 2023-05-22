#~/bin/bash

programs=(hz hz hz hz-mc)

for ((i=0; i<${#programs[@]}; i++)); do
    program=${programs[i]}
    name="$program-$i"
    if ! $(screen -list | grep $name > /dev/null); then
        echo "Starting $name..."
        if (( i != 3 )); then
            screen -S $name -d -m $program start -c hazelcast.yaml
        else
            screen -S $name -d -m $program start
        fi
    fi
done


