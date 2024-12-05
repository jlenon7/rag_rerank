from collections.abc import Sequence
from src.splitters import create_parent_splitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser 
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

def load_pdf_chunks(file_name: str, chunk_size: int, chunk_overlap: int):
  loader = PyPDFLoader(f"storage/{file_name}.pdf", extract_images=False)
  pages = loader.load_and_split()

  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    length_function=len,
    add_start_index=True
  )

  return text_splitter.split_documents(pages)

def load_code_folder_documents(
    path: str, 
    glob: str, 
    suffixes: Sequence[str], 
    exclude: Sequence[str] = None, 
    language: Language = None
):
   loader = GenericLoader.from_filesystem(
    f"storage/repositories/{path}",
    glob=glob,
    suffixes=suffixes,
    exclude=exclude,
    parser=LanguageParser(language=language, parser_threshold=500)
  )

   return loader.load()

def load_code_folder_chunks(
    path: str, 
    glob: str, 
    suffixes: Sequence[str], 
    chunk_size: int,
    chunk_overlap: int,
    exclude: Sequence[str] = None, 
    language: Language = None
):
  documents = load_code_folder_documents(path, glob, suffixes, exclude, language)
  splitter = create_parent_splitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, language=language)

  return splitter.split_documents(documents)
