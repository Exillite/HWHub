from fastapi import APIRouter

router = APIRouter()

@router.get("/hi", description="hi endpoint")
async def root():
    return {"message": "Hello, World!"}
