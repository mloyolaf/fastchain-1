from fastapi import APIRouter, Depends
from api.templates.dependencies import get_template_variables
from api.templates.dataclasses import TemplateVariables

router = APIRouter()
    
@router.get("/{prompt_id}")
async def read(prompt_id):
    return { 'prompt': prompt_id }

@router.put("/{prompt_id}")
async def update(variables: TemplateVariables, template_variables = Depends(get_template_variables)):
    return template_variables

@router.delete("/{prompt_id}")
async def delete(prompt_id):
    return { 'prompt': prompt_id }
