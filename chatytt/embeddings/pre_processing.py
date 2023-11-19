from langchain.text_splitter import RecursiveCharacterTextSplitter

from chatytt.conf.config import load_config

pre_processing_conf = load_config()["embeddings"]["pre_processing"]


def get_recursive_character_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=pre_processing_conf["recursive_character_splitting"]["chunk_size"],
        chunk_overlap=pre_processing_conf["recursive_character_splitting"][
            "chunk_overlap"
        ],
    )
