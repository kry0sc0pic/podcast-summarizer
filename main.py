import streamlit as st
from helpers import get_video_id, get_transcript, create_uuid
from dotenv import load_dotenv
from elevenlabslib import *
from config import LLMSettings, TextToSpeechSettings
from openai import OpenAI
import os

# Load Environment Variables (Keys)
load_dotenv()

# Streamlit Page Config (Icon/Title)
st.set_page_config(
    page_title="Podcast Summarizer",
    page_icon="🎙️",
)

# OpenAI Client (Cached)
@st.cache_resource(show_spinner=False)
def get_openai_client(show_spinner=False):
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return client


# ElevenLabs Voice (Cached)
@st.cache_resource(show_spinner=False)
def get_elevenlabs_voice():
    settings = TextToSpeechSettings()
    client = ElevenLabsUser(os.environ.get("ELEVENLABS_API_KEY"))
    voice = client.get_voices_by_name_v2(settings.get_voice_name())[0]
    return (client,voice)


# LLM Summary (Output Cached)
@st.cache_data(show_spinner=False)
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
    return summary.choices[0].message.content


# TTS (Output Cached)
@st.cache_data(show_spinner=False)
def get_tts_audio(summary: str) -> str:
    user,voice = get_elevenlabs_voice()
    settings = TextToSpeechSettings()
    generated = voice.generate_audio_v2(summary,settings.get_gen_options())
    savePath = f"outs/{generated[1]}.mp3"
    save_audio_v2(generated[0],savePath,outputFormat="mp3")
    if settings.should_auto_delete():
        historyItem = user.get_history_item(generated[1])
        historyItem.delete()
    return savePath


st.header("🎙 Podcast Summarizer")

link = st.text_input("Youtube Link (`youtube.com` or `youtu.be`)")

if st.button("Summarize"):
    vid = get_video_id(link)
    if vid is None:
        st.error("Invalid Link")

    else:
        with st.expander('Youtube Video',expanded=True):
            st.video(f"https://www.youtube.com/watch?v={vid}")
        with st.spinner("Fetching transcript"):
            transcript = get_transcript(vid)
        if transcript is None:
            st.error("Transcript not available")
        else:
            with st.expander('Transcript'):
                st.write(transcript)
            try:
                with st.spinner("Summarizing"):
                    summary = get_llm_summary(transcript)
                with st.expander('Summary'):
                    st.write(summary)
                try:
                    with st.spinner("Generating Audio"):
                        audio = get_tts_audio(summary)
                    st.audio(audio)
                except Exception as e:
                    st.error("Error generating audio")
                    print(e)
            except Exception as e:
                st.error("Error summarizing podcast")
                print(e)
