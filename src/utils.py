import os
import sys
from dotenv import load_dotenv

load_dotenv();

def get_database_url(TEST = False):
    if TEST:
        return os.getenv("DATABASE_TEST_URL");
    return os.getenv("DATABASE_URL");