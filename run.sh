#!/bin/bash

export PYTHONDONTWRITEBYTECODE=1

if [[ "$1" == "-PROD" ]]; then
    python3 ./src/main.py

elif [[ "$1" == "-TEST" ]]; then

    if ! command -v docker &> /dev/null; then
        echo "O Docker não está instalado. Por favor, instale o Docker e tente novamente."
        exit 1
    fi
    
    if [[ -f .env ]]; then
        source .env
    else
        echo "O arquivo .env não foi encontrado."
        exit 1
    fi
    
    echo "PREPARANDO AMBIENTE DE TESTES ..."
    docker stop "$POSTGRES_TEST_DB" > /dev/null 2>&1 && docker rm "$POSTGRES_TEST_DB" > /dev/null 2>&1
    docker run --name "$POSTGRES_TEST_DB" -e POSTGRES_PASSWORD=postgres -p 5433:5432 -d postgres > /dev/null 2>&1
    echo "RODANDO OS TESTES ..."
    sleep 2 && pytest src/tests.py
else
    python3 ./src/main.py
fi