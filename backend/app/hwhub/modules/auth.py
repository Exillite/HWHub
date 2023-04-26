from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Union

from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from .. import crud
from .. import schemas

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v0.1/auth/token")


router = APIRouter(
    prefix="/api/v0.1/auth",
    responses={404: {"description": "Not found"}},
    tags=["auth"],
)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(login: str):
    usr_mdl = crud.get_user_by_login(login)
    if usr_mdl:
        return schemas.UserInDB(id=str(usr_mdl.pk), 
                                login=usr_mdl.login, 
                                password=usr_mdl.password,
                                role=usr_mdl.role,
                                name=usr_mdl.name,
                                surname=usr_mdl.surname,
                                patronymic=usr_mdl.patronymic,
                                email=usr_mdl.email,
                                vk_id=usr_mdl.vk_id,
                                telegram_id=usr_mdl.telegram_id,
                                students_groups=usr_mdl.students_groups if usr_mdl.students_groups else [],
                                is_active=usr_mdl.is_active)

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
    user = schemas.User(id=str(current_user.id), 
                        login=current_user.login, 
                        role=current_user.role,
                        name=current_user.name,
                        surname=current_user.surname,
                        patronymic=current_user.patronymic,
                        email=current_user.email,
                        vk_id=current_user.vk_id,
                        telegram_id=current_user.telegram_id,
                        students_groups=current_user.students_groups if current_user.students_groups else [],
                        is_active=current_user.is_active)
    return user


@router.post("/token", response_model=schemas.Token)
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
