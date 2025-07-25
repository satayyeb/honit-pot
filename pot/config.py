import os

from pot.models import Service, ServiceType
from pot.singleton import SingletonABCMeta

import yaml


class Config(metaclass=SingletonABCMeta):
    base_url: str
    services: list[Service] = []

    def __init__(self, config_file_path: str | None = None):
        if not config_file_path:
            self.handle_single_mode()

        else:
            with open(config_file_path, 'r') as stream:
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

    def handle_single_mode(self):
        name = os.environ.get('SERVICE_NAME')
        type = os.environ.get('SERVICE_TYPE')
        id = os.environ.get('SERVICE_ID')
        token = os.environ.get('SERVICE_TOKEN')
        port = os.environ.get('SERVICE_PORT')

        if not (name and type and id and token and port):
            raise Exception('Environment variables missing.')

        self.services.append(
            Service(
                name=name,
                type=type,
                id=int(id),
                token=token,
                port=int(port),
            )
        )
