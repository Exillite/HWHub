from fastapi import FastAPI
import uvicorn
from envparse import Env
from fastapi.middleware.cors import CORSMiddleware

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from fastapi import Depends

from hwhub import schemas
from hwhub import models

from hwhub.modules import auth, user, student_group, homework, submission


env = Env()
MONGODB_URL = env.str("MONGODB_URL", default="mongodb://localhost:27017/test_database")


app = FastAPI(
    title="HWHub",
    description="API for application for manage homework assignments and their delivery by students.",
    version="0.1",
    contact={
        "name": "Author: Alexander Rodionov",
        "email": "alexander@rodionov.space"
    },
    openapi_url="/api/v0.1/openapi.json",
    redoc_url= None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v0.1/me", description="Check auth", tags=['BASE'])
async def read_users_me(
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    return {"status": 200, "user": current_user}


@app.get("/api/v0.1", description="Root endpoint", tags=['BASE'])
async def test():
    return {"message": "Hello World!"}


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(student_group.router)
app.include_router(homework.router)
app.include_router(submission.router)


async def connecct_to_mondodb():
    client = AsyncIOMotorClient(MONGODB_URL)
    await init_beanie(database=client.get_default_database(), document_models=models.__db_models__)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
