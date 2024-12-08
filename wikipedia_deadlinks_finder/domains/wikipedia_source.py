from dataclasses import dataclass
from enum import Enum


class WikipediaSourceStatus(Enum):
    ACTIVE = 1
    DEAD = 2
    UNDETERMINED = 3


@dataclass
class WikipediaSource:
    url: str
    status: WikipediaSourceStatus  # all links start as undetermined
