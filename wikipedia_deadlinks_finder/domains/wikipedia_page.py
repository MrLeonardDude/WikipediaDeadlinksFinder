from dataclasses import dataclass
from wikipedia_deadlinks_finder.domains.wikipedia_source import WikipediaSource


@dataclass
class WikipediaPage:
    url: str
    sources: list[WikipediaSource]
    content: str = ""  # Starts as null
