import src.personas as personas
from langchain_chroma import Chroma
from langchain.storage import LocalFileStore
from langchain_core.prompts import ChatPromptTemplate
from langchain.retrievers import ParentDocumentRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain.storage._lc_store import create_kv_docstore
from langchain.chains.retrieval import create_retrieval_chain
from src.splitters import create_child_splitter, create_parent_splitter
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever

def base_insert_chunks(chunks, embedding, directory="text_index"):
  Chroma.from_documents(chunks, embedding=embedding, persist_directory=f"storage/{directory}")

def parent_insert_documents(documents, embedding, chunk_size, chunk_overlap):
  child_splitter = create_child_splitter(chunk_size=chunk_overlap)
  parent_splitter = create_parent_splitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  parent_retriever = get_parent_retriever(
    embedding=embedding,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
  )

  parent_retriever.add_documents(documents, ids=None)

def get_vector_db(embedding, directory="text_index"):
  return Chroma(embedding_function=embedding, persist_directory=f"storage/{directory}")

def get_parent_retriever(embedding, child_splitter, parent_splitter):
  parentvectorstore = create_kv_docstore(LocalFileStore("storage/parent_chunks"))
  childvectorstore = Chroma(embedding_function=embedding, persist_directory="storage/child_chunks")

  return ParentDocumentRetriever(
    docstore=parentvectorstore,
    vectorstore=childvectorstore,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
  )


def base_ask(question, llm, embedding):
  vector_db = get_vector_db(embedding)
  retriever = vector_db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3}
  )

  documents = retriever.invoke(question)
  prompt = ChatPromptTemplate.from_messages([
    ("system", personas.athenna_docs_guru()),
    ("user", "{input}")
  ])

  document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
  retrieval_chain = create_retrieval_chain(retriever, document_chain)

  result = retrieval_chain.invoke({ "input": question, "context": documents })

  return result, documents

def parent_ask(question, llm, embedding, chunk_size, chunk_overlap):
  child_splitter = create_child_splitter(chunk_size=chunk_overlap)
  parent_splitter = create_parent_splitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  parent_retriever = get_parent_retriever(
    embedding=embedding,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
  )

  prompt = ChatPromptTemplate.from_messages([
    ("system", personas.athenna_docs_guru()),
    ("user", "{input}")
  ])

  setup_retrieval = RunnableParallel({"input":RunnablePassthrough(), "context": parent_retriever})
  output_parser = StrOutputParser()

  # So cool 🤩
  parent_chain_retrieval = setup_retrieval | prompt | llm | output_parser

  return parent_chain_retrieval.invoke(question)

def compressor_ask(question, llm, rerank, embedding):
  vector_db = get_vector_db(embedding)
  base_retriever = vector_db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 10}
  )

  compressor_retriever = ContextualCompressionRetriever(
    base_compressor=rerank,
    base_retriever=base_retriever
  )

  prompt = ChatPromptTemplate.from_messages([
    ("system", personas.price_analyzer()),
    ("user", "{input}")
  ])

  setup_retrieval = RunnableParallel({"input":RunnablePassthrough(),"context":compressor_retriever})
  output_parser = StrOutputParser()

  compressor_retrieval_chain = setup_retrieval | prompt | llm | output_parser

  return compressor_retrieval_chain.invoke(question)
