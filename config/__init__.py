class LLMSettings:
    def __init__(self):
        self.model = 'gpt-3.5-turbo-0125s'
        self.temperature = 0.7
        self.system_prompt = """You are a bot that summarized podcasts given a transcript by the user.
        """

    def get_model(self):
        return self.model

    def get_temperature(self):
        return self.temperature

    def get_system_prompt(self):
        return self.system_prompt


class TextToSpeechSettings:
    def __init__(self):
        self.voice = 'Rachel'

    def get_voice_name(self):
        return self.voice
