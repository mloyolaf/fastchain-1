from pydantic import BaseModel, Field
from langchain.pydantic_v1 import BaseModel as PBM
from typing import List, Optional

class VariableClassifier(PBM):
    "Según las variables presentes en el texto, clasificar."

    variables: str
    "Variables que se encuentran en el texto. Hacen referencia a una temática, tono o etc."

class PromptData(BaseModel):
    template_id: int = Field(
        default=...,
        description="ID of the template"
    )
    description: str = Field(
        default=...,
        description="Description to be used by LLMRouterChain"
    )
    system_variables: dict = Field(
        default=...,
        description="Dict of template variables",
        examples=[{'tone': "mean", 'form': "succint"}]
    )

class ChatRequest(BaseModel):
    prompts: List[PromptData] = Field(
        default=...,
        description="Prompts data"
    )
    question: str = Field(
        default=...,
        description="question"
    )
