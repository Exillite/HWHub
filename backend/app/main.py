from fastapi import FastAPI
import uvicorn
from mongoengine import connect
from envparse import Env
from fastapi.middleware.cors import CORSMiddleware

from fastapi import Depends

from hwhub import schemas

from hwhub.modules import auth, user


env = Env()
MONGODB_URL = env.str("MONGODB_URL", default="mongodb://localhost:27017/test_database")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/me", description="Check auth")
async def read_users_me(
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    return {"status": 200, "user": current_user}


@app.get("/api/v0.1", description="Root endpoint")
async def root():
    return {"message": "Hello World!"}


app.include_router(auth.router)
app.include_router(user.router)

connect(host=MONGODB_URL)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
