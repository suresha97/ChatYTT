from typing import Optional, List

from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.schema.vectorstore import VectorStore

from chatytt.conf.config import load_config
from chatytt.chains.base_chain import BaseChain
from chatytt.vector_store.pinecone_db import PineconeDB

chain_conf = load_config()["chains"]


class ConversationalQAChain(BaseChain):
    def __init__(
        self,
        vector_store: VectorStore,
        model_name: Optional[str] = None,
        temperature: float = 0.0,
    ):
        super().__init__()
        self.model_name = model_name if model_name else chain_conf["model_name"]
        self.temperature = temperature
        self.llm = OpenAI()
        self.vector_store = vector_store
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm, retriever=self.get_retriever()
        )

    def get_response(self, query: str, context: List[tuple[str, str]]):
        return self.chain({"question": query, "chat_history": context})["answer"]

    def get_retriever(self):
        return self.vector_store.as_retriever()


if __name__ == "__main__":
    load_dotenv()

    pinecone_db = PineconeDB(
        index_name="youtube-transcripts", embedding_source="open-ai"
    )

    # query = (
    #     "What was the turning point in Alex Hormozi's life that allowed him to become a successful"
    #     "business man ?"
    # )

    # template = (
    #     "Combine the chat history and follow up question into "
    #     "a standalone question. Chat History: {chat_history}"
    #     "Follow up question: {question}"
    # )
    # prompt = PromptTemplate.from_template(template)
    # llm = OpenAI()
    # question_generator_chain = LLMChain(llm=llm, prompt=prompt)

    query = (
        "Is buying a house a good financial decision to make in your 20s ? Give details on the "
        "reasoning behind your answer. Also provide the name of the speaker in the provided context from"
        "which you have constructed your answer."
    )
    chat_history: List[tuple[str, str]] = []

    conversational_qa_chain = ConversationalQAChain(
        vector_store=pinecone_db.vector_store
    )
    response = conversational_qa_chain.get_response(query=query, context=chat_history)
    print(response)

    chat_history = [(query, response)]
    query = "What is his opinion on what the right time to buy a house is then ?"

    response = conversational_qa_chain.get_response(query=query, context=chat_history)
    print(response)
