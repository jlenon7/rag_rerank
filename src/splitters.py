from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

def create_parent_splitter(chunk_size: int, chunk_overlap: int, language: Language = None):
  if language is None:
    return RecursiveCharacterTextSplitter(
      chunk_size=chunk_size,
      chunk_overlap=chunk_overlap,
      length_function=len,
      add_start_index=True
    )
  else:
    return RecursiveCharacterTextSplitter.from_language(
      language=language,
      chunk_size=chunk_size,
      chunk_overlap=chunk_overlap,
      length_function=len,
      add_start_index=True
    ) 

def create_child_splitter(chunk_size: int):
  return RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_size / 20)
