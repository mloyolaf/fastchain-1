from fastapi import APIRouter, Depends
from src.api.templates.template import router as template_router
from src.api.templates import dataclasses
from src.db.orm import models
from src.db.orm import get_db
import os
from sqlalchemy import select
from sqlalchemy.orm import Session

path = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

router = APIRouter(
    prefix=f"/{path}",
    tags=[path]
    
)

router.include_router(template_router)

@router.get("/", response_model=list[dataclasses.ReadResponse])
async def templates_read(db: Session = Depends(get_db)):
    stmt = select(models.Template)
    return [dataclasses.ReadResponse.from_orm(row) for row in db.scalars(stmt)]

@router.post("/", response_model=dataclasses.CreateResponse)
async def template_create(template: dataclasses.CreateRequest, db: Session = Depends(get_db)):
    instance = models.Template(**template.model_dump())
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return dataclasses.CreateResponse.from_orm(instance)#utils.template.create_template(templates)
