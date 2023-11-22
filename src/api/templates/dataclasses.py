from typing import Literal, List, Optional, ClassVar
from pydantic import BaseModel, Field

#create_model("Response", id=(int, ...), __base__=dataclasses.Template)

class ReadResponse(BaseModel):
    template: str = Field(
        default=...,
        description="System template"
    )
    template_type: Literal["human", "system", "ai"] = Field(
        default=...,
        description="Type for the template"
    )
    template_id: Optional[int] = Field(
        default=None,
        description="ID of the next template in the flow."
    )
    id: int = Field(
        default=...,
        description="Id of the updated template"
    )
    class Config:
        from_attributes = True

class CreateRequest(BaseModel):
    template: str = Field(
        default="{text}",
        examples=["You are a very {personality} assistant who answers in a very {tone} way."],
        description="System template"
    )
    template_type: Literal["human", "system", "ai"] = Field(
        default=...,
        examples=["human", "system", "ai"],
        description="Type for the template"
    )
    template_id: Optional[int] = Field(
        default=None,
        description="ID of the next template in the flow."
    )
    class Config:
        from_attributes = True

class CreateResponse(BaseModel):
    id: int = Field(
        default=...,
        description="Id of the created template"
    )
    class Config:
        from_attributes = True

class UpdateRequest(BaseModel):
    template: Optional[str] = Field(
        default=None,
        description="System template"
    )
    template_type: Optional[Literal["human", "system", "ai"]] = Field(
        default=None,
        examples=["human", "system", "ai"],
        description="Type for the template"
    )
    template_id: Optional[int] = Field(
        default=None,
        description="ID of the next template in the flow."
    )
    class Config:
        from_attributes = True
    
class Templates(BaseModel):
    templates: List[ReadResponse] = Field(
        default=...,
        description="Human, system or AI prompts."
    )
    class Config:
        from_attributes = True

class Variable(BaseModel):
    variable: str = Field(
        default=...,
        description="Value to fill the template variable with."
    )
    
class Variables(BaseModel):
    variables: List[Variable] = Field(
        default=...,
        description="Values to fill the template variable with."
    )
