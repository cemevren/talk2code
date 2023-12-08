from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import qdrant_client
from pydantic import BaseModel
from app.settings import settings
from app.libs.qa import QA
from langchain.vectorstores.qdrant import Qdrant
from app.libs.embedding_model import get_embedding_model


app = FastAPI()

embedding_model = get_embedding_model()
qdrant_client_inst = qdrant_client.QdrantClient(
    url=settings.qdrant_url,
)
qdrant = Qdrant(
    client=qdrant_client_inst, embeddings=embedding_model, collection_name="langchain"
)

qa = QA(vector_store=qdrant)


class InferenceRequest(BaseModel):
    id: str
    user_message: str


@app.post("/api/completion")
async def openai_streaming(request: InferenceRequest):
    try:
        stream = qa.completion(user_message=request.user_message)
        return StreamingResponse(content=stream, media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI call failed, {e}")
