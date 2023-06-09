#!/bin/bash

export PYTHONDONTWRITEBYTECODE=1

# ----------------------------------------------------------------

if [[ -f .env ]]; then
    source .env
else
    echo "ERRO: O arquivo de configuração .env não foi encontrado." && exit 1
fi

# ----------------------------------------------------------------

start_service() {
    service=$1
    status_var="has_${service}"

    if systemctl is-active --quiet $service; then
        eval $status_var=true
    else
        echo "INFO:     Tentando iniciar o serviço $service"
        sudo systemctl start $service
        if systemctl is-active --quiet $service; then
            echo "INFO:     Serviço $service inicializado com sucesso"
            eval $status_var=true
        else
            echo "INFO:     Falha ao inicializar o serviço $service"
            eval $status_var=false
        fi
    fi
}

has_postgresql=false
has_docker=false

start_service "postgresql"
start_service "docker"

# ----------------------------------------------------------------

create_docker_database() {

    database="$1"
    port="$2"
    docker stop "$database" > /dev/null 2>&1
    docker rm "$database" > /dev/null 2>&1
    docker run --name "$database" -e POSTGRES_PASSWORD=postgres -p "$port":5432 -v db_data:/var/lib/postgresql/data -d postgres > /dev/null 2>&1

    if docker inspect -f '{{.State.Running}}' "$database" >/dev/null 2>&1; then
        return 0 # success
    else
        return 1
    fi
}

startup_error() {
    echo "ERRO: É necessário ter Postgres ou Docker instalado e em execução."
    exit 1
}

docker_error()
{
    echo "ERRO: Falha ao criar o contêiner Docker."
    exit 1
}

# ----------------------------------------------------------------

if [[ "$1" == "-DOCKER" ]]; then
    if ! "$has_docker"; then
        echo "ERRO: É necessário ter o Docker instalado e rodando."
        exit 1
    fi

    echo "INFO:     Rodando a aplicação em container docker."
    docker-compose down && docker-compose up --build

# ----------------------------------------------------------------

elif [[ "$1" == "-TEST" ]]; then
    if "$has_postgresql"; then
        echo "INFO:     Rodando os testes no banco de dados local"
            pytest
    elif "$has_docker"; then
        echo "INFO:     Rodando os testes no banco de dados docker"
        if create_docker_database "$POSTGRES_TEST_DB" "5432"; then # 5433
            sleep 2 && pytest
        else
            echo "ERRO: Falha ao criar o contêiner Docker."
            exit 1
        fi
    else
        startup_error
    fi

# ----------------------------------------------------------------

else
    if "$has_postgresql"; then
        echo "INFO:     Rodando a aplicação no banco de dados local"
        python3 ./src/main.py
    elif "$has_docker"; then
        echo "INFO:     Rodando a aplicação no banco de dados docker"
        if create_docker_database "$POSTGRES_DB" "5432"; then
            sleep 2 && python3 ./src/main.py
        else
            echo "ERRO: Falha ao criar o contêiner Docker."
            exit 1
        fi
    else
        startup_error
    fi
fi
