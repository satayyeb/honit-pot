import requests

from pot.config import Config
from pot.models import Service



class LLMApi:
    def __init__(self, service: Service, session_base: bool=False):
        self.service = service
        self.session_base = session_base
        self.session_id = 0
        self.history = []  # TODO: Remove from here and move to the subclass

    def chat(self, message: str) -> str:
        try:
            resp = requests.post(
                url=Config().base_url + f'/api/v1/services/{self.service.id}/sessions/{self.session_id}/router',
                json={
                    'request': message,
                    'token': self.service.token
                }
            ).json()
            if self.session_base:
                self.session_id = resp['session_id']
            return resp['response']
        except Exception as e:
            print(e)
            return ''

