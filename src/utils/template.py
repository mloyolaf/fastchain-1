
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_distances
from langchain.embeddings import OpenAIEmbeddings
# from transformers import AutoTokenizer, AutoModel
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.api.templates.dataclasses import Templates
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import os
from dotenv import load_dotenv

from langchain.embeddings import OpenAIEmbeddings
load_dotenv() 
api_key = os.getenv('OPENAI_API_KEY')

embeddings_model = OpenAIEmbeddings()

route = "C:/Users/mloyolaf/OneDrive - NTT DATA EMEAL/Escritorio/Ignacia/NTT DATA Argentina/Galicia-seguros/Script/Asistente-cliente/Main/Src"
documents_data = pd.read_pickle(route+"/documents_data_openai.pickle")

def create_template(templates: Templates) -> ChatPromptTemplate:
    all_templates = []
    for template in templates.templates:
        if template.template_type == "human":
            all_templates.append(HumanMessagePromptTemplate.from_template(template.template))
        elif template.template_type == "system":
            all_templates.append(SystemMessagePromptTemplate.from_template(template.template))
        else:
            all_templates.append(AIMessagePromptTemplate.from_template(template.template))
        
    chat_prompt = ChatPromptTemplate.from_messages(all_templates)
    return chat_prompt

def popul8_template():
    return True


def process_documents(route_documents): 
    document = PyPDFLoader(route_documents)
    data = document.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        length_function = len,
        chunk_overlap=250
    )
    documents = text_splitter.split_documents(data)
    return documents

# def create_embeddings(texts):
#     # Cargar el modelo y el tokenizador
#     model_name = 'bert-base-multilingual-cased'
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModel.from_pretrained(model_name)

#     # Tokenizar los textos y convertirlos a tensores
#     inputs = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')

#     # Obtener los embeddings
#     with torch.no_grad():
#         outputs = model(**inputs)
#         embeddings = outputs.last_hidden_state.mean(dim=1)

#     # Convertir los embeddings a una matriz numpy
#     embeddings = embeddings.numpy()

#     return embeddings






def get_embeddings_openai( text:str,embeddings_model=embeddings_model):
        embd = np.array(embeddings_model.embed_query(text))
        return embd

def question_user(q:str):
  data_question = pd.DataFrame()
  emb = []
  q_list = []
  emb.append(get_embeddings_openai(q))
  q_list.append(q)
  data_question["pregunta"] = q_list
  data_question["embedding_pregunta"] = emb
  return data_question

def documents_prompt(documents:list, pages:list):
    docs = []
    for doc in range(len(documents)):
        val_aux = documents[doc].metadata["page"]
        if val_aux in pages:
            docs.append(documents[doc])
        else:
            continue
    return docs

# Función que retorna una lista con las páginas que va a recibir el prompt
def get_pages(data:object, name_page:str, col_name:str):
    pages_content = []
    index_col = data.columns.get_loc(col_name)
    for index in range(data.shape[0]):
        val = data.iloc[index, index_col]
        pages_content.append(val["page"])
        pages_content = sorted(list(set(pages_content)))
    return pages_content

def data_metadata_documentation(data:pd.DataFrame,data_p:pd.DataFrame):
    data["distance_cos"] = data["embeddings_content"].apply(lambda x: cosine_distances(data_p.loc[0,"embedding_pregunta"].reshape(1,-1), x.reshape(1,-1)))
    data = data.sort_values(by = "distance_cos",ascending=False)
    return data

def function_main_get_documents(documents:list, question_human:str,data_document = documents_data):
    question = question_user(question_human)
    documents_ = data_metadata_documentation(data_document, question)
    pages = get_pages(documents_, "page","metadata")
    docs_ = documents_prompt(documents, pages)
    return docs_[:10]






