#!/bin/bash

export PYTHONDONTWRITEBYTECODE=1

if [[ "$1" == "-PROD" ]]; then
    python3 main.py
else
    uvicorn main:app --reload --port 3000
fi
