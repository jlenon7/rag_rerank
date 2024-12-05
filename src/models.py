from os import environ
from langchain_openai import ChatOpenAI
from langchain_cohere import CohereRerank
from langchain_openai import OpenAIEmbeddings

def create_llm_model():
  return ChatOpenAI(
    max_tokens=200,
    model_name="gpt-3.5-turbo",
    api_key=environ.get("OPENAI_API_KEY")
  )

def create_embedding_model():
  return OpenAIEmbeddings(
    api_key=environ.get("OPENAI_API_KEY"),
    model="text-embedding-3-small",
    disallowed_special=()
  )

def create_rerank_model(top_n = 3):
  return CohereRerank(
    top_n=top_n, 
    model="rerank-v3.5",
    cohere_api_key=environ.get("COHERE_API_KEY")
  )
