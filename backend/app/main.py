from fastapi import FastAPI
import uvicorn
from mongoengine import connect
from envparse import Env

from hwhub import crud
from hwhub import schemas
from hwhub import validations

from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing_extensions import Annotated


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

env = Env()
MONGODB_URL = env.str("MONGODB_URL", default="mongodb://localhost:27017/test_database")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

router = APIRouter(
    prefix="/api/v0.1",
    responses={404: {"description": "Not found"}},
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(login: str):
    usr_mdl = crud.get_user_by_login(login)
    if usr_mdl:
        return schemas.UserInDB(pk=str(usr_mdl.pk), login=usr_mdl.login, password=usr_mdl.password)

def authenticate_user(login: str, password: str):
    user = get_user(login)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user)
):
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/")
async def read_users_me(
    current_user: schemas.User = Depends(get_current_active_user)
):
    return current_user


@app.post("/register")
async def registaration(user: schemas.UserCreate):
    pwd = str(user.password)
    try:
        user.password = get_password_hash(pwd)
    except Exception as e:
        print(e)
    nu = crud.create_user(user)
    return {"nu_id": nu.login}


@app.get("/users/me/items/")
async def read_own_items(
    current_user: schemas.User = Depends(get_current_active_user)
):
    return [{"item_id": "Foo", "owner": current_user.pk}]


@router.get("/", description="Root endpoint")
async def root():
    return {"message": "Hello Wodrld!"}


app.include_router(router)

connect(host=MONGODB_URL)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
