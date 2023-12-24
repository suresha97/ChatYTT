from typing import List

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import BaseChatModel
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.vectorstore import VectorStore
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

from chatytt.conf.config import load_config
from chatytt.chains.base_chain import BaseChatChain
from chatytt.vector_store.pinecone_db import PineconeDB
from chatytt.chains.custom.doc_retrieval_lcel_chain import DocRetrievalLCELChain

chain_conf = load_config()["chains"]
load_dotenv()


class ConversationalQASequentialChain(BaseChatChain):
    def __init__(
        self, vector_store: VectorStore, chat_model: BaseChatModel, top_k_docs: int = 5
    ):
        super().__init__()
        self.chat_model = chat_model
        self.vector_store = vector_store
        self.top_k_docs = top_k_docs

    def get_response(self, query: str, chat_history: List) -> str:
        chat_history = convert_messages_to_chat(chat_history)
        seq_chain = SequentialChain(
            chains=[
                self.condense_chat_history_and_question_chain,
                self.retrieve_context_chain,
                self.retrieve_answer_chain,
            ],
            input_variables=["question", "chat_history", "top_k", "vector_store"],
            output_variables=["text"],
            verbose=True,
        )

        return seq_chain.run(
            question=query,
            chat_history=chat_history,
            top_k=self.top_k_docs,
            vector_store=self.vector_store,
        )

    @property
    def condense_chat_history_and_question_chain(self):
        return LLMChain(
            llm=self.chat_model,
            prompt=condense_query_prompt(),
            output_parser=StrOutputParser(),
            output_key="query",
        )

    @property
    def retrieve_context_chain(self):
        return DocRetrievalLCELChain()

    @property
    def retrieve_answer_chain(self):
        return LLMChain(
            llm=self.chat_model,
            prompt=retrieval_qa_prompt(),
            output_parser=StrOutputParser(),
        )


def condense_query_prompt():
    _template = """Given the following conversation and a follow up question, rephrase the
     follow up question to be a standalone question, in its original language.

    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:"""

    return PromptTemplate.from_template(_template)


def retrieval_qa_prompt():
    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    return ChatPromptTemplate.from_template(template)


def convert_messages_to_chat(chat_history):
    if not len(chat_history):
        return " "

    chat = []
    for input in chat_history:
        human_msg, ai_msg = input
        chat.append(f"Human: {human_msg}")
        chat.append(f"AI: {ai_msg}")

    return "\n".join(chat)


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

    conversational_qa_chain = ConversationalQASequentialChain(
        vector_store=pinecone_db.vector_store, chat_model=ChatOpenAI(temperature=0.0)
    )
    response = conversational_qa_chain.get_response(
        query=query, chat_history=chat_history
    )
    print(response)

    chat_history = [(query, response)]
    query = "What is his opinion on what the right time to buy a house is then ?"

    response = conversational_qa_chain.get_response(
        query=query, chat_history=chat_history
    )
    print(response)

    chat_history.append((query, response))
    query = "Why do so many people recommend buying one ?"
    response = conversational_qa_chain.get_response(
        query=query, chat_history=chat_history
    )
    print(response)
