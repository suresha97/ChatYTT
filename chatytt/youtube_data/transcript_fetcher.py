import time
from typing import List

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter, JSONFormatter

from chatytt.youtube_data.data_models import FormattedVideoTranscript


class TranscriptFetcher:
    def __init__(self, formatting_method: str):
        self.formatting_method = formatting_method
        self.transcript_formatter = _formatting_method_to_formatter_map[
            self.formatting_method
        ]()

    def get_batch_formatted_video_transcripts(
        self, video_ids: List[str]
    ) -> List[FormattedVideoTranscript]:
        formatted_transcripts = []

        for video_id in video_ids:
            transcript = self.get_formatted_video_transcript(video_id)
            formatted_transcripts.append(transcript)

            time.sleep(3)

        return formatted_transcripts

    def get_formatted_video_transcript(self, video_id: str) -> FormattedVideoTranscript:
        raw_transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatted_transcript = self.format_transcript(raw_transcript)

        transcript = {
            "video_id": video_id,
            "formatting_method": self.formatting_method,
            "transcript": formatted_transcript,
        }

        return FormattedVideoTranscript.model_validate(transcript)

    def format_transcript(self, raw_transcript):
        return self.transcript_formatter.format_transcript(raw_transcript)


_formatting_method_to_formatter_map = {"json": JSONFormatter, "text": TextFormatter}
