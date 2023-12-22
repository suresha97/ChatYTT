from typing import List
import os

from dotenv import load_dotenv

from chatytt.youtube_data.transcript_fetcher import TranscriptFetcher
from chatytt.youtube_data.data_models import FormattedVideoTranscript
from chatytt.utils.s3 import (
    list_keys_at_prefix_dir_level,
    load_json_from_s3_as_dict,
    save_json_to_s3,
)
from chatytt.conf.config import load_config


def get_most_recent_video_id_collection_timestamp():
    video_id_keys = list_keys_at_prefix_dir_level(
        bucket="chatyt-youtube-data",
        filter_prefix_dir=f"video-ids/" f"{os.environ.get('PLAYLIST_NAME')}-video-ids/",
    )
    max_timestamp_key = max([int(timestamp_key) for timestamp_key in video_id_keys])

    return max_timestamp_key


def store_latest_transcripts(
    transcripts: List[FormattedVideoTranscript], video_id_retrieval_timestamp: int
):
    if len(transcripts):
        for transcript in transcripts:
            save_json_to_s3(
                json_obj=dict(transcript),
                bucket="chatyt-youtube-data",
                key=f"video-transcripts/"
                f"{os.environ.get('PLAYLIST_NAME')}-transcripts/"
                f"{video_id_retrieval_timestamp}/"
                f"{transcript.video_id}.json",
            )
    else:
        save_json_to_s3(
            json_obj={},
            bucket="chatyt-youtube-data",
            key=f"video-transcripts/"
            f"{os.environ.get('PLAYLIST_NAME')}-transcripts/"
            f"{video_id_retrieval_timestamp}/"
            "null_transcript.json",
        )


def lambda_handler(event, context):
    load_dotenv()

    transcript_conf = load_config()["youtube_data"]["transcript"]

    max_timestamp_key = get_most_recent_video_id_collection_timestamp()
    latest_video_ids = load_json_from_s3_as_dict(
        bucket="chatyt-youtube-data",
        key=f"video-ids/"
        f"{os.environ.get('PLAYLIST_NAME')}-video-ids/"
        f"{max_timestamp_key}"
        f"/video_ids.json",
    )["video_ids"]

    transcript_fetcher = TranscriptFetcher(
        formatting_method=transcript_conf["formatting_method"]
    )
    transcripts = transcript_fetcher.get_batch_formatted_video_transcripts(
        latest_video_ids
    )

    store_latest_transcripts(
        transcripts, video_id_retrieval_timestamp=max_timestamp_key
    )


if __name__ == "__main__":
    lambda_handler({}, None)
