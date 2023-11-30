from fastapi import APIRouter, Depends
from dotenv import load_dotenv
from langchain.schema import AIMessage, HumanMessage
from src.api.models  import router as models_router
from src.api.context import router as context_router
from src.api.templates import router as prompts_router
from src.api.dataclasses import ChatRequest, VariableClassifier
from src.db.orm.models import Template
from src.db.orm import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate
)
from langchain.chat_models import AzureChatOpenAI
from langchain.schema.runnable import RunnableBranch
from langchain.output_parsers.openai_functions import PydanticAttrOutputFunctionsParser
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

from operator import itemgetter
import os

path = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

router = APIRouter(
    prefix=f"/{path}"
)

router.include_router(models_router)
router.include_router(prompts_router)
router.include_router(context_router)

load_dotenv() 
api_key = os.getenv('OPENAI_API_KEY')
model = AzureChatOpenAI(temperature=0, deployment_name="chat")

@router.get("/")
async def index():
    return { "path": path }

@router.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    # Si el request tiene más de un template, entonces usar condicional, sino
    # usar el prompt directamente
    chat_messages = []
    branches = []

    default_template =  ChatPromptTemplate.from_template(
        "You are a helpful assistant. Answer the question as accurately as you can.\n\n{input}"
    )
    
    for template_data in request.prompts:
        stmt = select(Template).where(Template.id == template_data.template_id)
        template: Template = db.scalar(stmt)
        chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(template.system_template.format(**template_data.system_variables)),
            HumanMessagePromptTemplate.from_template(template.human_template),
            #AIMessagePromptTemplate.from_template(template.ai_template) el AIMessage lo usaré para los examples
        ])
        messages = chat_prompt.format_prompt(**template_data.system_variables,
                                             input = request.question).to_messages()

        chain = (chat_prompt | model)
        branches.append((lambda x: x['variables'] in template_data.system_variables.values(), chat_prompt))
        #chat_messages.append(messages)

    classifier_function = convert_pydantic_to_openai_function(VariableClassifier)
    llm = model.bind(
        functions=[classifier_function], function_call={"name": "VariableClassifier"}
    )
    parser = PydanticAttrOutputFunctionsParser(
        pydantic_schema=VariableClassifier, attr_name="variables"
    )
    classifier_chain = llm | parser
    branches.append(default_template)
    try:
        final_chain = (
            RunnablePassthrough.assign(variables=itemgetter("input") | classifier_chain)
            | RunnableBranch(*branches)
            | model
            | StrOutputParser()
        )
        return final_chain.invoke({"input": request.question})
    except Exception as e:
        import traceback
        print(traceback.print_exc())
        print(tuple(branches))
    
