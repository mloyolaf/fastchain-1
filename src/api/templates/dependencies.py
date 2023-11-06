from typing import Annotated
from fastapi import Path, Body
from api.templates.dataclasses import (
    TemplateVariable, TemplateVariables
)

def get_template_variables(prompt_id: Annotated[str, Path(...)], variables: Annotated[TemplateVariables, Body(...)]):
    # TODO: si los resultados de traer las variables del template del prompt
    # coinciden con los variables del request body
    #return TemplateVariables(variables=[TemplateVariable(variable=prompt_id)])
    print(variables.model_fields.keys())
    return variables
