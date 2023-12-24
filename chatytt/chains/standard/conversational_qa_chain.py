from typing import Optional, List

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.schema.vectorstore import VectorStore

from chatytt.conf.config import load_config
from chatytt.chains.base_chain import BaseChatChain
from chatytt.vector_store.pinecone_db import PineconeDB

chain_conf = load_config()["chains"]


class ConversationalQAChain(BaseChatChain):
    def __init__(
        self,
        vector_store: VectorStore,
        model_name: Optional[str] = None,
        temperature: float = 0.0,
    ):
        super().__init__()
        self.model_name = model_name if model_name else chain_conf["model_name"]
        self.temperature = temperature
        self.llm = ChatOpenAI()
        self.vector_store = vector_store
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm, retriever=self.get_retriever()
        )

    def get_response(self, query: str, chat_history: List[tuple[str, str]]):
        return self.chain({"question": query, "chat_history": chat_history})["answer"]

    def get_retriever(self):
        return self.vector_store.as_retriever()


if __name__ == "__main__":
    load_dotenv()

    pinecone_db = PineconeDB(
        index_name="youtube-transcripts", embedding_source="open-ai"
    )

    query = (
        "Is buying a house a good financial decision to make in your 20s ? Give details on the "
        "reasoning behind your answer. Also provide the name of the speaker in the provided context from"
        "which you have constructed your answer."
    )
    chat_history: List[tuple[str, str]] = []

    conversational_qa_chain = ConversationalQAChain(
        vector_store=pinecone_db.vector_store
    )
    response = conversational_qa_chain.get_response(
        query=query, chat_history=chat_history
    )
    print(response)

    chat_history = [(query, response)]
    query = "What is his opinion on what the right time to buy one is ?"

    response = conversational_qa_chain.get_response(
        query=query, chat_history=chat_history
    )
    print(response)
