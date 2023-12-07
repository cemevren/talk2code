from app.libs.embedding_model import get_embedding_model
from app.libs.qdrant_client import get_qdrant_client
from app.libs.loader import RepoLoader


def load():
    embedding_model = get_embedding_model()
    vector_store = get_qdrant_client(embedding_model, "langchain")
    vector_store.client.delete_collection(collection_name="langchain")

    print(vector_store)
    loader = RepoLoader(
        path="./data/github/langchain",
        embedding_model=embedding_model,
        vector_store=vector_store,
    )
    loader.load()


if __name__ == "__main__":
    load()
