import os
import openai

class TextGenerator:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key

    async def generate_message(self, messages, temperature=0):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=temperature
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error occurred while calling OpenAI API: {e}")
            return "ごめんね、APIの調子が悪いみたい。\nタイマーは問題なく動作してるから、引き続きがんばってね！"
