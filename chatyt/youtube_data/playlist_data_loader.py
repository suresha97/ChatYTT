import os
from typing import List, Dict

from youtube_api.youtube_api import YoutubeDataApi

from youtube_data.utils import APIKeyNotFoundError
from youtube_data.data_models import VideoMetadataFromAPI


class PlaylistDataLoader:
    def __init__(self):
        self.youtube_data_api = YoutubeDataApi(key=self.try_get_api_key())

    # TODO
    def get_recent_video_ids_from_playlist(self, start_date, end_date):
        raise NotImplementedError

    def get_video_ids_from_playlist(self, playlist_id: str) -> Dict[str, List[str]]:
        video_metadata = self.get_video_metadata_from_playlist(playlist_id)
        video_ids = parse_video_ids(video_metadata)

        return video_ids

    def get_video_metadata_from_playlist(
        self, playlist_id: str
    ) -> List[VideoMetadataFromAPI]:
        video_metadata = self.youtube_data_api.get_videos_from_playlist_id(
            playlist_id=playlist_id
        )

        return [
            VideoMetadataFromAPI.model_validate(metadata) for metadata in video_metadata
        ]

    def try_get_api_key(self):
        key = os.environ.get("YOUTUBE_DATA_API_KEY", default=None)
        if key:
            return key
        else:
            raise APIKeyNotFoundError("No API key found for youtube-data-api!")


def parse_video_ids(video_metadata: List[VideoMetadataFromAPI]):
    video_ids = [vid.video_id for vid in video_metadata]

    return {"video_ids": video_ids}
