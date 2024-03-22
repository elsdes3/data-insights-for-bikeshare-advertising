#!/bin/bash


ACTION=${1:-get-data}


if [[ "$ACTION" != 'reset'* ]]; then
    echo "Waiting for 5 seconds..."
    sleep 5
    echo "Done."
    docker logs -t $(docker ps --filter "name=${ACTION}" --format "{{.ID}}")
else
    docker rmi $(docker images -a --filter "reference=*${ACTION:6}*" --format "{{.ID}}")

    cd notebooks
    if [[ "$ACTION" == 'reset-get-data' ]]; then
        cd 01-get-data
    else
        cd 02-eda
    fi

    cd notebooks
    rm -rf .ipynb_checkpoints/

    cd ../../../src

    rm -rf __pycache__/
fi
