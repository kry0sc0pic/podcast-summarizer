# 🎙️ Podcast Summarizer



## Setup (Non-Docker)
0. create api keys for openai and eleven labs
1. copy `.env.example` to `.env` and fill in the necessary values
![ENV Sample](docs/env.png)
2. install dependencies `pip install -r requirements.txt`
3. run the app `streamlit run main.py`
4. open the browser and go to `http://localhost:8501`

## Setup (Docker)
0. create api keys for openai and eleven labs
1. build the docker image `docker build -t podcast-summarizer .`
2. run the docker container

```
docker run -p 8080:8080 \
-e OPENAI_API_KEY=<openai_api_key> \
-e ELEVENLABS_API_KEY=<elevenlabs_api_key> \ podcast-summarizer
``````

3. open the browser and go to `http://localhost:8080`

## Configuration Options
All configuration options are in `config/__init__.py`

LLM Configuration

*chunk_size should not be greater than the context length*
![LLM Config Screenshot](docs/llm.png)

TTS Configuration
![TTS SEttings](docs/tts.png)

