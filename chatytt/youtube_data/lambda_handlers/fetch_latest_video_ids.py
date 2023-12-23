import time
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

from chatytt.youtube_data.playlist_data_loader import PlaylistDataLoader
from chatytt.utils.s3 import save_json_to_s3
from chatytt.conf.config import load_config


def lambda_handler(event, context):
    load_dotenv()

    video_conf = load_config()["youtube_data"]["video"]

    playlist_data_loader = PlaylistDataLoader()
    video_ids = playlist_data_loader.get_recent_video_ids_from_playlist(
        playlist_id=video_conf["playlist_id"],
        lookback_datetime=datetime.now()
        - timedelta(days=video_conf["latest_video_lookback_delta_days"]),
    )

    save_json_to_s3(
        video_ids,
        bucket="chatyt-youtube-data",
        key=f"video-ids/"
        f"{os.environ.get('PLAYLIST_NAME')}-video-ids/"
        f"{int(time.time())}/"
        f"video_ids.json",
    )


if __name__ == "__main__":
    lambda_handler({}, None)
