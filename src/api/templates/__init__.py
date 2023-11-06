from fastapi import APIRouter
from api.templates.template import router as prompt_router
from api.templates.dataclasses import Prompts
import utils.template
import os

path = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

router = APIRouter(
    prefix=f"/{path}"
)

router.include_router(prompt_router)

@router.get("/")
async def read():
    return { "path": path }

@router.post("/")
async def create(prompts: Prompts):
    return utils.template.create_template(prompts)
