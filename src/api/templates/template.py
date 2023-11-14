from fastapi import APIRouter, Depends
from api.templates.dependencies import get_template_variables
from api.templates import dataclasses
from db.orm import get_db
from db.orm import models
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

router = APIRouter(dependencies=[])
    
@router.get("/{template_id}", response_model=dataclasses.ReadResponse)
async def template_read(template_id, db: Session = Depends(get_db)):
    stmt = (
        select(models.Template)
        .where(models.Template.id == template_id)
    )
    return dataclasses.ReadResponse.from_orm(db.scalar(stmt))
    
@router.put("/{template_id}", response_model=dataclasses.ReadResponse)
async def template_update(template_id, template: dataclasses.UpdateRequest, db: Session = Depends(get_db)):
    stmt = (
        update(models.Template)
        .where(models.Template.id == template_id)
        .values(template.model_dump())
        #.returning(models.Template) not supported in sqlite < 3.35
    )
    db.execute(stmt)
    db.commit()
    stmt = (
        select(models.Template)
        .where(models.Template.id == template_id)
    )
    return dataclasses.ReadResponse.from_orm(db.scalar(stmt))

@router.delete("/{template_id}")
async def template_delete(template_id, db: Session = Depends(get_db)):
    try:
        stmt = (
            delete(models.Template)
            .where(models.Template.id == template_id)
            #.returning(models.Template) not supported in sqlite < 3.35
        )
        db.execute(stmt)
        db.commit()
    finally:
        return "OK"

@router.patch("/{template_id}")
async def expand(variables: dataclasses.Variables, template_variables = Depends(get_template_variables)):
    return template_variables
