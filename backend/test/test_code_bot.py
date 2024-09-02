import pytest
import qdrant_client
from langchain.vectorstores.qdrant import Qdrant
from app.libs.embedding_model import get_embedding_model
from app.libs.qa import QA
from app.settings import Settings

settings = Settings()

user_message = "Which function should I use to split a python file to chunks?"
embedding_model = get_embedding_model()
client = qdrant_client.QdrantClient(
    url="http://localhost:6333",
)
qdrant = Qdrant(client=client, embeddings=embedding_model, collection_name="langchain")

qa = QA(vector_store=qdrant)


def test_retrieve_code():
    retriever = qdrant.as_retriever(
        search_type=settings.vector_search_type,
        search_kwargs={"k": settings.vector_search_k},
    )

    result = retriever.get_relevant_documents(user_message)
    # print(result)
    assert len(result) == 4


@pytest.mark.asyncio
async def test_code_bot():
    stream = qa.completion(user_message=user_message)
    reply = ""
    async for chunk in stream:
        if chunk is not None:
            reply += chunk

    print(reply)

    len_system_messages = 0
    len_user_messages = 0
    len_assistant_messages = 0

    for message in qa.history:
        if message["role"] == "system":
            len_system_messages += 1
        elif message["role"] == "user":
            len_user_messages += 1
        elif message["role"] == "assistant":
            len_assistant_messages += 1

    assert len_system_messages == 2
    assert len_user_messages == 1
    assert len_assistant_messages == 1
