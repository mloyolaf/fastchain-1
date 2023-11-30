from fastapi import APIRouter, Depends
from src.api.templates.dependencies import get_template_variables
from src.api.templates import dataclasses
from src.db.orm import get_db
from src.db.orm import models
from src.utils.template import process_documents,function_main_get_documents
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
import pandas as pd


route_file = "C:/Users/mloyolaf/OneDrive - NTT DATA EMEAL/Escritorio/Ignacia/NTT DATA Argentina/Galicia-seguros/Script/Asistente-cliente/Main/documents/Poliza 2465274 celu.pdf"
route = "C:/Users/mloyolaf/OneDrive - NTT DATA EMEAL/Escritorio/Ignacia/NTT DATA Argentina/Galicia-seguros/Script/Asistente-cliente/Main/Src"
data_documents = pd.read_pickle(route+"/documents_data_openai.pickle")

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
        .values({key: val for key, val in template.model_dump().items() if val is not None})
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


@router.post("/{process_documents}/")
async def documents_prompt_(question_human:str):
    documents = process_documents(route_file)
    docs_ = function_main_get_documents(documents, question_human)
    return {"documents":docs_}
