from fastapi import APIRouter

from app.hwhub.crud import *

router = APIRouter()

@router.get("/hi", description="hi endpoint")
async def root():
    return {"message": "Hello, World!"}
