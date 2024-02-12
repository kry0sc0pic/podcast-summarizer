from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import streamlit as st
from uuid import uuid4
transcript_formatter = TextFormatter()

@st.cache_data
def get_video_id(link: str) -> str | None:
    if link.startswith("https://www.youtube.com/watch?v="):
        return link.split("https://www.youtube.com/watch?v=")[1].split("&")[0]
    elif link.startswith("https://youtu.be/"):
        return link.split("https://youtu.be/")[1]
    return None

@st.cache_data
def get_transcript(id: str) -> str | None:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(id)
        transcript = transcript_formatter.format_transcript(transcript)
        return transcript
    except Exception as e:
        return None

def create_uuid():
    return uuid4().hex
