import requests
from bs4 import BeautifulSoup
from app.config import OTOMOTO_HEADERS, REQUEST_TIMEOUT

class Scraper:
    def __init__(self):
        # Search BMW E46 in Dolny Śląsk region (region_id=10)
        self.url = "https://www.otomoto.pl/osobowe/bmw/dolnoslaskie?search%5Bfilter_float_price%3Ato%5D=10000&search%5Blat%5D=51.232&search%5Blon%5D=16.907&search%5Badvanced_search_expanded%5D=true"
        self.headers = OTOMOTO_HEADERS
    
    def fetch_offers_html(self):
        """Fetch OTOMOTO page and return BeautifulSoup object"""
        try:
            response = requests.get(
                self.url,
                headers=self.headers,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching OTOMOTO: {e}")
            return None
    
    def get_offer_articles(self, soup):
        """Extract all offer article elements from page"""
        if not soup:
            return []
        
        articles = soup.find_all('article')
        return articles
