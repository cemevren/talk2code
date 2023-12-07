from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.embeddings import Embeddings
from app.prompts import prompts
from app.settings import settings


def get_embedding_model() -> Embeddings:
    return HuggingFaceBgeEmbeddings(
        model_name=settings.embedding_model_name,
        model_kwargs={"device": settings.embedding_model_device},
        encode_kwargs={
            "normalize_embeddings": True
        },  # set True to compute cosine similarity
        query_instruction=prompts["EMBED_QUERY_INSTRUCTION"],
    )
