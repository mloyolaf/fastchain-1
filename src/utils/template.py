from api.templates.dataclasses import Prompts
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

def create_template(prompts: Prompts) -> ChatPromptTemplate:
    templates = []
    for template in prompts.templates:
        if template.prompt_type == "human":
            templates.append(HumanMessagePromptTemplate.from_template(template.content))
        elif template.prompt_type == "system":
            templates.append(SystemMessagePromptTemplate.from_template(template.content))
        else:
            templates.append(AIMessagePromptTemplate.from_template(template.content))
        
    chat_prompt = ChatPromptTemplate.from_messages(templates)
    return chat_prompt

def popul8_template():
    return True
