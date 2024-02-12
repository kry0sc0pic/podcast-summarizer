import streamlit as st
from helpers import get_video_id, get_transcript
from dotenv import load_dotenv
from elevenlabslib import *
from config import LLMSettings, TextToSpeechSettings
from openai import OpenAI
import os

load_dotenv()

st.set_page_config(
    page_title="Podcast Summarizer",
    page_icon="🎙️",
)

@st.cache_resource
def get_openai_client():
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return client

@st.cache_resource
def get_elevenlabs_client():
    settings = TextToSpeechSettings()
    client = ElevenLabsUser(
        api_key=os.environ.get("ELEVENLABS_API_KEY")
    )
    voice = client.get_voice_by_name_v2(settings.get_voice_name())


@st.cache_data
def get_llm_summary(transcript: str) -> str:
    client = get_openai_client()
    settings = LLMSettings()
    summary = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": settings.get_system_prompt(),
            },
            {
                "role": "user",
                "content": f"""Transcript
                {transcript}""",
            }
        ],
        model=settings.get_model(),
    )

st.header("🎙 Podcast Summarizer")

link = st.text_input("Youtube Link")

if st.button("Summarize"):
    vid = get_video_id(link)
    if vid is None:
        st.error("Invalid Link")
    else:
        transcript = get_transcript(vid)
        if transcript is None:
            st.error("Transcript not available")
        else:
            st.write(transcript)
