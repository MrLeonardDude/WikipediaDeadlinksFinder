from wikipedia_deadlinks_finder.use_cases.find_all_deadlink_sources import (
    find_all_deadlink_sources,
)
from wikipedia_deadlinks_finder.domains.wikipedia_page import WikipediaPage

from wikipedia_deadlinks_finder.infrastructure.wikipedia_client.request_wikipedia_client import (
    RequestWikipediaClient,
)
from wikipedia_deadlinks_finder.infrastructure.sources_client.request_source_client import (
    RequestSourceClient,
)
from asyncio import run

from dotenv import load_dotenv
from os import environ

async def main():
    wikipedia_page_input = WikipediaPage(
        url=environ.get('PAGE_URL'), # TODO might do a CLI input idk... might do a cronjob that gets a bunch of urls and pastes to this page
        sources=[],
    )

    wikipedia_client = RequestWikipediaClient()
    source_client = RequestSourceClient()
    await find_all_deadlink_sources(wikipedia_page_input, wikipedia_client, source_client)
    
    await source_client.close()


if __name__ == "__main__":
    load_dotenv()
    # TODO add some super fancy cool check for connectivities with the many resources REDIS and the main callback if this becomes a EVENT/MESSSAGE consumer
    run(main())
