import time
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

from chatytt.youtube_data.playlist_data_loader import PlaylistDataLoader
from chatytt.utils.s3 import save_json_to_s3


if __name__ == "__main__":
    load_dotenv()

    playlist_data_loader = PlaylistDataLoader()
    video_ids = playlist_data_loader.get_recent_video_ids_from_playlist(
        playlist_id=str(os.environ.get("PLAYLIST_ID")),
        lookback_datetime=datetime.now() - timedelta(weeks=2),
    )

    save_json_to_s3(
        video_ids,
        bucket=str(os.environ.get("YOUTUBE_DATA_BUCKET")),
        key=f"{os.environ.get('VIDEO_IDS_KEY_PREFIX')}/"
        f"{os.environ.get('PLAYLIST_NAME')}-video-ids/"
        f"{int(time.time())}/"
        f"video_ids.json",
    )
