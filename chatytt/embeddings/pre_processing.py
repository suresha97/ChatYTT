from langchain.text_splitter import RecursiveCharacterTextSplitter


def get_recursive_character_splitter():
    return RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=10)
