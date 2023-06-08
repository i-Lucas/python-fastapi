import uvicorn
from fastapi import FastAPI
from utils import get_database_url

app = FastAPI()

@app.get("/")
def say_hello():
    return "hello, python!"

print(get_database_url())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)