from fastapi import APIRouter
from .model import router as model_router
import os

path = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

router = APIRouter(
    prefix=f"/{path}"
)

router.include_router(model_router)

@router.get("/")
async def index():
    return { "path": path }
