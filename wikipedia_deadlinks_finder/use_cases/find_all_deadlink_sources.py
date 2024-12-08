from wikipedia_deadlinks_finder.domains.wikipedia_page import WikipediaPage
from wikipedia_deadlinks_finder.domains.wikipedia_source import WikipediaSourceStatus

from wikipedia_deadlinks_finder.utils.logger import logger

from asyncio import gather


async def check_source_and_set_status(source, source_client):
    is_valid = await source_client.validate_source(source)
    if not is_valid:
        source.status = WikipediaSourceStatus.DEAD
        return

    source.status = WikipediaSourceStatus.ACTIVE


# TOOD do big fancy assync to try to ask if source is valid with all assync
async def find_all_deadlink_sources(
    wikipedia_page_input: WikipediaPage, wikipedia_client, source_client
) -> bool:
    """Finds all deadlink sources in a given wikipedia website page

    A source will be defined as a deadlink if at least three attemps fail when trying to fetch it
    """
    logger.info("getting page content...")
    content_enriched_page = wikipedia_client.get_wikipedia_page(wikipedia_page_input)

    result_status = {
        WikipediaSourceStatus.ACTIVE: 0,
        WikipediaSourceStatus.DEAD: 0,
    }
    await gather(
        *[
            check_source_and_set_status(source, source_client)
            for source in content_enriched_page.sources
        ]
    )
    
    for source in wikipedia_page_input.sources:
        result_status[source.status] += 1

    logger.info(f"logging wikipedia page sources results... {result_status}")

    return True
