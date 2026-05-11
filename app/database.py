import sqlite3
from datetime import datetime
from app.config import DB_PATH

class Database:
    def __init__(self):
        self.db_path = DB_PATH
        self.init_db()
    
    def init_db(self):
        """Create database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS offers (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            price INTEGER,
            year INTEGER,
            mileage INTEGER,
            location TEXT,
            url TEXT NOT NULL,
            image_url TEXT,
            score INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notified BOOLEAN DEFAULT 0
        )
        """)
        
        conn.commit()
        conn.close()
    
    def offer_exists(self, offer_id):
        """Check if offer already exists in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM offers WHERE id = ?", (offer_id,))
        exists = cursor.fetchone() is not None
        
        conn.close()
        return exists
    
    def save_offer(self, offer):
        """Save new offer to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO offers (id, title, price, year, mileage, location, url, score, notified)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            offer['id'],
            offer['title'],
            offer['price'],
            offer['year'],
            offer['mileage'],
            offer['location'],
            offer['url'],
            offer['score'],
            1  # Mark as notified
        ))
        
        conn.commit()
        conn.close()
    
    def get_all_offers(self, limit=20):
        """Get recent offers from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT id, title, price, year, mileage, location, url, score, created_at
        FROM offers
        ORDER BY created_at DESC
        LIMIT ?
        """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_offer_count(self):
        """Get total number of offers in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM offers")
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
