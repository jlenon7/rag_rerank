from src.langchain import load_pdf_chunks 
from src.vector import base_insert_chunks
from src.models import create_embedding_model

embedding = create_embedding_model()

chunks = load_pdf_chunks(
  file_name="tarkov_ammo",
  chunk_size=4000,
  chunk_overlap=20
)

base_insert_chunks(chunks=chunks, embedding=embedding, directory="base_db")
