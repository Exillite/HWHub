from fastapi import FastAPI
import uvicorn
from mongoengine import connect
from envparse import Env



env = Env()
MONGODB_URL = env.str("MONGODB_URL", default="mongodb://localhost:27017/test_database")

app = FastAPI()


@app.get("/", description="Root endpoint")
async def root():
    return {"message": "Hello Word"}



connect(host=MONGODB_URL)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)