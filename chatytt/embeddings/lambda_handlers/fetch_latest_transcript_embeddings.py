import os

from dotenv import load_dotenv

from chatytt.utils.s3 import list_keys_at_prefix_dir_level
from chatytt.embeddings.s3_json_document_loader import S3JsonFileLoader
from chatytt.embeddings import pre_processing
from chatytt.vector_store.pinecone_db import PineconeDB
from chatytt.conf.config import load_config


def get_latest_transcript_file_keys():
    transcript_keys = list_keys_at_prefix_dir_level(
        bucket="chatyt-youtube-data",
        filter_prefix_dir=f"video-transcripts/"
        f"{os.environ.get('PLAYLIST_NAME')}-transcripts/",
    )
    max_timestamp_key = max([int(timestamp_key) for timestamp_key in transcript_keys])

    file_filter_prefix = (
        "video-transcripts/"
        + f"{os.environ.get('PLAYLIST_NAME')}-transcripts/"
        + f"{max_timestamp_key}/"
    )

    latest_transcript_files = list_keys_at_prefix_dir_level(
        bucket="chatyt-youtube-data",
        filter_prefix_dir=file_filter_prefix,
    )

    return [
        file_filter_prefix + file
        for file in latest_transcript_files
        if file != "null_transcript.json"
    ]


def lambda_handler(event, context):
    load_dotenv()
    pinecone_conf = load_config()["pinecone_db"]

    latest_transcript_file_keys = get_latest_transcript_file_keys()

    docs = []
    for file_key in latest_transcript_file_keys:
        loader = S3JsonFileLoader(
            bucket="chatyt-youtube-data",
            key=file_key,
            text_splitter=pre_processing.get_recursive_character_splitter(),
        )

        docs.extend(loader.load(split_doc=True))

    if len(docs):
        vector_store = PineconeDB(
            index_name=pinecone_conf["index_name"],
            embedding_source=pinecone_conf["embedding_source"],
        )
        vector_store.save_documents_as_embeddings(docs)


if __name__ == "__main__":
    lambda_handler({}, None)
