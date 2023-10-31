#!/bin/bash

if [[ -z "$1" || $1 == "null" ]]; then
    echo "Version is valid"
    exit 0
else
    echo "ABORTING: Version already exists"
    echo "ABORTING: Change the version.yaml file"
    exit 1
fi
