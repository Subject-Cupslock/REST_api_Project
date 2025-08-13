##тестовый роут для проверки работоспособности
from fastapi import APIRouter 

router = APIRouter()


@router.get("/ping")
async def ping():
    return {"message": "pong"}