import requests
from bs4 import BeautifulSoup
import re
from src.logger_config import setup_logger

logger = setup_logger("Scraper")

def get_links(url):
    """
    Fetches the Wikipedia page at `url` and returns a list of valid Wikipedia article links.
    Returns a list of tuples: (title, full_url)
    """
    try:
        # Wikipedia requires a User-Agent header
        headers = {
            'User-Agent': 'WikipediaSpeedrunner/1.0 (https://github.com/yourusername/wikipedia-speedrunner; your@email.com)'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the main content div to avoid sidebar/footer links
        content_div = soup.find(id="mw-content-text")
        if not content_div:
            logger.warning(f"Could not find main content on page: {url}")
            return []

        links = set()
        
        # Regex to match valid wiki links (ignore files, special pages, etc.)
        # Valid: /wiki/Title
        # Invalid: /wiki/File:..., /wiki/Special:..., /wiki/Talk:..., /wiki/Help:...
        wiki_link_pattern = re.compile(r"^/wiki/((?!File:|Special:|Talk:|Help:|Category:|Portal:|Wikipedia:).+)")

        for a_tag in content_div.find_all('a', href=True):
            href = a_tag['href']
            match = wiki_link_pattern.match(href)
            if match:
                title = a_tag.get('title')
                if not title:
                    # Fallback to text content if title attribute is missing
                    title = a_tag.text.strip()
                
                if title:
                    full_url = f"https://en.wikipedia.org{href}"
                    links.add((title, full_url))
        
        logger.info(f"Scraped {len(links)} links from {url}")
        return list(links)

    except requests.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")
        return []
