import os
import sys
import time
from dotenv import load_dotenv

load_dotenv();

def get_test_url():
    return os.getenv("DATABASE_TEST_URL");

def get_docker_url():
    return os.getenv("DATABASE_URL_DOCKER");

def get_docker_test_url():
    return os.getenv("DATABASE_TEST_DOCKER_URL");

def get_database_url(TEST=False):
    docker_arg = len(sys.argv) > 1 and sys.argv[1] == "-DOCKER"
    
    if TEST: return get_test_url();
    elif docker_arg: return get_docker_url();
    return os.getenv("DATABASE_URL")
