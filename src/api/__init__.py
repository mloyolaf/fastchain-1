from fastapi import APIRouter
from api.models  import router as models_router
from api.context import router as context_router
from api.templates import router as prompts_router
import os

path = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

router = APIRouter(
    prefix=f"/{path}"
)

router.include_router(models_router)
router.include_router(prompts_router)
router.include_router(context_router)

@router.get(f"/")
async def index():
    return { "path": path }
