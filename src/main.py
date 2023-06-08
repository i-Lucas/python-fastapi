import uvicorn
from fastapi import FastAPI
from utils import get_database_url
from routes import coupon_router
from database import initialize_database

app = FastAPI();

@app.get("/")
def say_hello():
    return "hello, python!";

app.include_router(coupon_router);

def run_server():
    initialize_database(get_database_url());
    uvicorn.run(app, host="0.0.0.0", port=3000);

if __name__ == "__main__":
    run_server();