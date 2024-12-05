from src.vector import compressor_ask 
from src.models import create_llm_model, create_rerank_model, create_embedding_model

llm = create_llm_model()
rerank = create_rerank_model()
embedding = create_embedding_model()

result = compressor_ask(
  llm=llm, 
  rerank=rerank,
  embedding=embedding, 
  question="Which one is the powerful 5.56x45mm ammo?"
)

print(result)
