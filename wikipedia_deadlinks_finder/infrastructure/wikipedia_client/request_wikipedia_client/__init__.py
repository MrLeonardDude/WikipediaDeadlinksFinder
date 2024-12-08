from wikipedia_deadlinks_finder.domains.wikipedia_page import WikipediaPage
from wikipedia_deadlinks_finder.domains.wikipedia_source import (
    WikipediaSource,
    WikipediaSourceStatus,
)
from requests import Session
from bs4 import BeautifulSoup
from ipaddress import ip_address
from urllib.parse import urlparse


class RequestWikipediaClient:

    def __init__(self):
        self.session = Session()

    def __check_if_host_is_only_ip(self, url):
        try:
            # Parse the URL to extract the hostname
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname

            # Check if the hostname is a valid IP address
            ip_address(hostname)
            return True  # It's an IP address
        except ValueError:
            return False  # It's not an IP address

    def get_wikipedia_page(self, wikipedia_page: WikipediaPage) -> WikipediaPage:
        response = self.session.get(wikipedia_page.url)

        if response.status_code == 202:
            raise Exception("Wikipedia page wrong or unavailable at the moment")

        wikipedia_page.content = response.content

        # Parse the HTML
        soup = BeautifulSoup(wikipedia_page.content, "html.parser")

        # Find the div with class 'reflist' and saves its links inside WikipediaPage
        reflist_div = soup.find("div", class_="reflist")
        hrefs = []
        if reflist_div:
            wikipedia_page.sources = [
                WikipediaSource(a["href"], WikipediaSourceStatus.UNDETERMINED)
                for a in reflist_div.find_all("a", href=True)
                if "http" in a["href"]
                and not self.__check_if_host_is_only_ip(a["href"])
            ]

        return wikipedia_page
