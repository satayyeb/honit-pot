from benchmark.consts import OPENAI_BASE_URL, OPENAI_API_KEY
from benchmark.prompt import prompt_text
from openai import OpenAI

client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)


class LocalLLMApi:

    def __init__(self, model_name):
        self.model_name = model_name
        self.history = [{'role': 'system', 'content': prompt_text}]

    def chat(self, message: str) -> str:
        completion = client.chat.completions.create(
            model=self.model_name,
            extra_body={},
            messages=[
                *self.history,
                {'role': 'user', 'content': message},
            ]
        )
        reply = completion.choices[0].message.content
        self.history.append({'role': 'user', 'content': message})
        self.history.append({'role': 'assistant', 'content': reply})
        return reply
