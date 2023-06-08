#!/bin/bash

export PYTHONDONTWRITEBYTECODE=1

if [[ "$1" == "-PROD" ]]; then
    python3 ./src/main.py
else
    python3 ./src/main.py
fi
