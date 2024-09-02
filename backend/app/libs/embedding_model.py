from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.embeddings import Embeddings
from app.prompts import prompts
from app.settings import settings
import torch


def get_embedding_model() -> Embeddings:
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    return HuggingFaceBgeEmbeddings(
        model_name=settings.embedding_model_name,
        model_kwargs={"device": device},
        encode_kwargs={
            "normalize_embeddings": True
        },  # set True to compute cosine similarity
        query_instruction=prompts["EMBED_QUERY_INSTRUCTION"],
    )
