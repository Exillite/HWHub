from fastapi import FastAPI
import uvicorn
from mongoengine import connect
from envparse import Env
from fastapi.middleware.cors import CORSMiddleware

from hwhub.modules import auth

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


# @router.get("/users/me/")
# async def read_users_me(
#     current_user: schemas.User = Depends(get_current_active_user)
# ):
#     return current_user


# @router.post("/register")
# async def registaration(user: schemas.UserCreate):
#     pwd = str(user.password)
#     try:
#         user.password = get_password_hash(pwd)
#     except Exception as e:
#         print(e)
#     nu = crud.create_user(user)
#     return {"nu_id": nu.login}


@app.get("/api/v0.1", description="Root endpoint")
async def root():
    return {"message": "Hello World!"}


app.include_router(auth.router)

connect(host=MONGODB_URL)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
