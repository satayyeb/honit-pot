from dataclasses import dataclass
from enum import Enum


class ServiceType(Enum):
    K8S = 'K8S'
    SSH = 'SSH'

    @classmethod
    def from_string(cls, value):
        match value:
            case 'K8S':
                return cls.K8S
            case 'SSH':
                return cls.SSH
            case _:
                raise ValueError


@dataclass
class Service:
    name: str
    type: str
    id: int
    token: str
    port: int
