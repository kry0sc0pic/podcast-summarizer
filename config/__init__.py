from elevenlabslib import PlaybackOptions,GenerationOptions
class LLMSettings:
    def __init__(self):
        self.model = 'gpt-3.5-turbo-0125'
        self.temperature = 0.7
        self.chunk_size = 15000 # if transcript is longer, it will be split into chunks of this size
        self.system_prompt = """You are a bot that summarizes podcasts given a transcript by the user. Transcripts may be in one message or split across multiple messages
        """

    def get_model(self):
        return self.model

    def get_temperature(self):
        return self.temperature

    def get_system_prompt(self):
        return self.system_prompt


class TextToSpeechSettings:
    def __init__(self):
        # Voice name to use (if multiple voices are available, it will use the first one from the results)
        self.voice = 'Rachel'

        # Generation Options for the Summary
        self.generation_settings = {
            "model": 'eleven_monolingual_v1',
            "use_speaker_boost": True,
            "stability": 0.3,
            "similarity_boost": 0.7,
            "style": 0
        }

        # Generation Options Object for ElevenLabs
        self.generation_options = GenerationOptions(
            **self.generation_settings
        )

        # Deletes Audio from ElevenLabs after generation
        self.auto_delete = True


    def get_voice_name(self):
        return self.voice

    def get_gen_options(self):
        return self.generation_options

    def should_auto_delete(self):
        return self.auto_delete
