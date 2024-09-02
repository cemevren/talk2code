from typing import AsyncGenerator

from langchain.vectorstores import VectorStore
from app.libs.llm_model import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionUserMessageParam,
)
from app.settings import settings
from app.prompts import prompts
from app.libs.llm_model import LLMModel


class QA:
    def __init__(self, vector_store: VectorStore):
        initial_system_message = ChatCompletionSystemMessageParam(
            content=prompts["INIT_SYS_PROMPT"],
            role="system",
        )
        self.history: list[ChatCompletionMessageParam] = [initial_system_message]
        self.vector_store = vector_store
        self.llm_model = LLMModel()

    async def add_retriver_result(self, user_message: str):
        retriever = self.vector_store.as_retriever(
            search_type=settings.vector_search_type,
            search_kwargs={"k": settings.vector_search_k},
        )

        result = await retriever.aget_relevant_documents(user_message)
        self.history.append(
            ChatCompletionSystemMessageParam(
                content="Related code:\n\n".join(
                    [
                        f"{doc.page_content}\n{doc.metadata}\n====\n\n"
                        for i, doc in enumerate(result)
                    ]
                ),
                role="system",
            )
        )

    async def completion(
        self, user_message: str
    ) -> AsyncGenerator[str, ChatCompletionAssistantMessageParam]:
        await self.add_retriver_result(user_message)

        message = ChatCompletionUserMessageParam(content=user_message, role="user")
        self.history.append(message)

        stream = self.llm_model.completion_stream(history=self.history)

        # Stream responses
        reply = ""
        async for chunk in stream:
            if chunk is not None:
                reply += chunk
                yield chunk

        message = ChatCompletionAssistantMessageParam(content=reply, role="assistant")

        self.history.append(message)
