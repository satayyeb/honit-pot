from models import Service
from singleton import SingletonABCMeta

import yaml


class Config(metaclass=SingletonABCMeta):
    base_url: str
    services: list[Service] = []

    def __init__(self):
        with open('config.yaml', 'r') as stream:
            config_yaml = yaml.safe_load(stream)
            self.base_url = config_yaml['base_url']
            for item in config_yaml['services']:
                self.services.append(
                    Service(
                        name=item['name'],
                        type=item['type'],
                        id=item['id'],
                        token=item['token'],
                        port=item['port'],
                    )
                )
