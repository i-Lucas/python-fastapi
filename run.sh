#!/bin/bash

export PYTHONDONTWRITEBYTECODE=1

if [[ "$1" == "-PROD" ]]; then
    python3 main.py
else
    python3 main.py
fi
