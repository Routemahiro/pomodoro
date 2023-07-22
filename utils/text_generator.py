# utils/text_generator.py
import os
import openai

class TextGenerator:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key

    def generate_message(self, messages, temperature=0):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature
        )
        return response["choices"][0]["message"]["content"]