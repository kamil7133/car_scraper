import time
import sys
from datetime import datetime
from app.config import SCRAPE_INTERVAL_SECONDS
from app.scraper import Scraper
from app.parser import Parser
from app.database import Database
from app.scoring import Scoring
from app.notifier import Notifier

class BMWOfferHunter:
    def __init__(self):
        self.scraper = Scraper()
        self.db = Database()
        self.run_count = 0
    
    def hunt(self):
        """Main hunting loop"""
        self.run_count += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'='*70}")
        print(f"🏹 HUNT #{self.run_count} - {timestamp}")
        print(f"{'='*70}")
        
        # Fetch page
        print("📥 Fetching OTOMOTO page...")
        soup = self.scraper.fetch_offers_html()
        if not soup:
            print("❌ Failed to fetch page")
            return 0
        
        # Get articles
        articles = self.scraper.get_offer_articles(soup)
        print(f"📦 Found {len(articles)} articles")
        
        if not articles:
            print("⚠️  No articles found")
            return 0
        
        # Parse and process
        new_offers = 0
        for i, article in enumerate(articles, 1):
            offer = Parser.parse_offer(article)
            
            if not offer:
                continue
            
            # Check if already exists
            if self.db.offer_exists(offer['id']):
                continue
            
            # Score the offer
            score = Scoring.score_offer(offer)
            offer['score'] = score
            
            # Save to database
            self.db.save_offer(offer)
            new_offers += 1
            
            # Send notification
            print(f"\n✨ NEW OFFER #{new_offers}:")
            print(f"  Title: {offer['title']}")
            print(f"  Price: {offer['price']:,} PLN" if offer['price'] else "  Price: N/A")
            print(f"  Year: {offer['year']}" if offer['year'] else "  Year: N/A")
            print(f"  Mileage: {offer['mileage']:,} km" if offer['mileage'] else "  Mileage: N/A")
            print(f"  Location: {offer['location']}" if offer['location'] else "  Location: N/A")
            print(f"  Score: {score}/100")
            print(f"  URL: {offer['url']}")
            
            Notifier.send_discord_notification(offer)
        
        # Summary
        total_offers = self.db.get_offer_count()
        print(f"\n📊 Summary:")
        print(f"  New offers: {new_offers}")
        print(f"  Total in DB: {total_offers}")
        
        return new_offers
    
    def run(self):
        """Run the hunter in loop"""
        print("\n")
        print("  ╔════════════════════════════════════════╗")
        print("  ║  🚗 BMW OFFER HUNTER - MVP v1.0       ║")
        print("  ║  Śląsk Edition                         ║")
        print("  ╚════════════════════════════════════════╝")
        print(f"\nInterval: {SCRAPE_INTERVAL_SECONDS} seconds")
        print(f"Database: {self.db.db_path}")
        print("\nPress CTRL+C to stop\n")
        
        try:
            while True:
                self.hunt()
                print(f"\n⏳ Next hunt in {SCRAPE_INTERVAL_SECONDS}s...")
                time.sleep(SCRAPE_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print("\n\n🛑 Hunter stopped")
            sys.exit(0)

def main():
    hunter = BMWOfferHunter()
    hunter.run()

if __name__ == "__main__":
    main()
