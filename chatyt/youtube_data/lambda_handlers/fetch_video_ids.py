import time
import os

from dotenv import load_dotenv

from youtube_data.playlist_data_loader import PlaylistDataLoader
from utils.s3 import save_json_to_s3


if __name__ == "__main__":
    load_dotenv()

    playlist_data_loader = PlaylistDataLoader()
    video_ids = playlist_data_loader.get_video_ids_from_playlist(
        playlist_id=str(os.environ.get("PLAYLIST_ID"))
    )

    save_json_to_s3(
        video_ids,
        bucket=str(os.environ.get("YOUTUBE_DATA_BUCKET")),
        key=f"{os.environ.get('VIDEO_IDS_KEY_PREFIX')}/{int(time.time())}/video_ids.json",
    )
