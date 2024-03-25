from fastapi import FastAPI
import os

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": f"Hello from the Api service!, DB_ENV: {os.getenv('DATABASE_URL') }"
    }
