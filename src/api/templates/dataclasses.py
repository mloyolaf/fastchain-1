from typing import Literal, List, Optional, ClassVar
from pydantic import BaseModel, Field

#create_model("Response", id=(int, ...), __base__=dataclasses.Template)

class ReadResponse(BaseModel):
    id: int = Field(
        default=...,
        description="Id of the updated template"
    )
    description: Optional[str] = Field(
        default=None,
        description="Description usage of temaplate"
    )
    system_template: str = Field(
        default=...,
        description="Set up agent personality.",
        examples=["You are a very {personality} assistant who answers in a very {tone} way."],
    )
    human_template: str = Field(
        default=...,
        description="User question.",
        examples=["{input}"],
    )
    ai_template: str = Field(
        default=...,
        description="Agent response.",
        examples=["{output}"],
    )
    class Config:
        from_attributes = True

class CreateRequest(BaseModel):
    description: Optional[str] = Field(
        default=None,
        description="Description usage of temaplate"
    )
    system_template: str = Field(
        default=...,
        description="Set up agent personality.",
        examples=["You are a very {personality} assistant who answers in a very {tone} way."],
    )
    human_template: str = Field(
        default="{input}",
        description="User question.",
        examples=["{input}"],
    )
    ai_template: str = Field(
        default="{output}",
        description="Agent response.",
        examples=["{output}"],
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
    description: Optional[str] = Field(
        default=None,
        description="Description usage of temaplate"
    )
    system_template: Optional[str] = Field(
        default=...,
        description="Set up agent personality.",
        examples=["You are a very {personality} assistant who answers in a very {tone} way."],
    )
    human_template: Optional[str] = Field(
        default="{input}",
        description="User question.",
        examples=["{input}"],
    )
    ai_template: Optional[str] = Field(
        default=...,
        description="Agent response.",
        examples=["{output}"],
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
