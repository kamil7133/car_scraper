import requests
from bs4 import BeautifulSoup
from app.config import OTOMOTO_BASE_URL, OTOMOTO_HEADERS, REQUEST_TIMEOUT

class Scraper:
    def __init__(self):
        self.url = OTOMOTO_BASE_URL
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
