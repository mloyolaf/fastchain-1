from typing import List, Optional, Any, Union
from pydantic import BaseModel, Field
from fastapi import APIRouter
#from langchain.output_parsers import PydanticOutputParser
from langchain.document_loaders import JSONLoader

#from .context import router as context_router
import os
import tempfile
import io

path = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

router = APIRouter(
    prefix=f"/{path}"
)

#router.include_router(context_router)

class Attribute(BaseModel):
    name: str = Field(
        default=...,
        description="Name of the attribute.",
        examples=["Name"]
    )
    #attr_type: Optional[str] = Field(
    #    default=None,
    #    description="Type of value used for validation.",
    #    examples=["question", "fact"]
    #) TODO: revosar esto para el OutputParser
    description: str = Field(
        default=...,
        description="Description of the field for the LLM to use for context.",
        examples=["Name of the user", "Product X"]
    )
    value: Union[Any, List[Any]] = Field(
        default=...,
        description="Single value or list of attributes of the same structure.",
        examples=["TODO"]
    )

class Attributes(BaseModel):
    attribute: List[Attribute]

def metadata_func(record: dict, metadata: dict) -> dict:

    print(record)
    metadata["description"] = record.get("description")
    metadata["attrib_name"] = record.get("name")

    return metadata
    
@router.get("/")
async def read():
    return { "path": path }

@router.post("/")
async def create(attributes: Attributes):
    tmp_json = tempfile.NamedTemporaryFile(mode="w", suffix=".json")
    tmp_json.write(attributes.model_dump_json())
    tmp_json.seek(0)
    loader = JSONLoader(
        file_path=os.path.abspath(tmp_json.name),
        jq_schema=".attribute[]",
        content_key="value",
        metadata_func=metadata_func,
        text_content=False
    )
    docs = loader.load()
    tmp_json.close()

    return docs
