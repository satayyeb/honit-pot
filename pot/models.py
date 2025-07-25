from dataclasses import dataclass
from enum import Enum


class ServiceType(Enum):
    K8S = 'K8S'
    SSH = 'SSH'


@dataclass
class Service:
    name: str
    type: ServiceType
    id: int
    token: str
    port: int
