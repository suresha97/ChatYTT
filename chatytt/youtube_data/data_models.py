from datetime import datetime

from pydantic import BaseModel


class VideoMetadataFromAPI(BaseModel):
    video_id: str
    channel_id: str
    publish_date: float  # UNIX timestamp
    collection_date: datetime


class FormattedVideoTranscript(BaseModel):
    video_id: str
    formatting_method: str
    transcript: str
