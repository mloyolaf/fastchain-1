from typing import Literal, List
from pydantic import BaseModel, Field

class Prompt(BaseModel):
    content: str = Field(
        default="{text}",
        examples=["You are a very {personality} assistant who answers in a very {tone} way."],
        description="System template"
    )
    prompt_type: Literal["human", "system", "ai"] = Field(
        default=...,
        examples=["human", "system", "ai"],
        description="Type for the template"
    )

class Prompts(BaseModel):
    templates: List[Prompt] = Field(
        default=...,
        description="Human, system or AI prompts."
    )

class TemplateVariable(BaseModel):
    variable: str = Field(
        default=...,
        description="Values to fill the template variable with."
    )
    
class TemplateVariables(BaseModel):
    variables: List[TemplateVariable] = Field(
        default=...,
        description="Values to fill the template variable with."
    )
