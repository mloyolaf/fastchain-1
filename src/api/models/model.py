from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

@router.get("/{model_id}")
async def read(model_id):
    return { 'model': model_id }

@router.put("/{model_id}")
async def update(model_id):
    return { 'model': model_id }

@router.delete("/{model_id}")
async def delete(model_id):
    return { 'model': model_id }
