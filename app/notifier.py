import requests
import json
from app.config import DISCORD_WEBHOOK_URL

class Notifier:
    @staticmethod
    def send_discord_notification(offer):
        """Send offer notification to Discord via webhook"""
        if not DISCORD_WEBHOOK_URL:
            print("⚠️  Discord webhook not configured, skipping notification")
            return False
        
        try:
            # Build embed
            embed = {
                "title": f"🔥 NOWA OFERTA BMW",
                "description": offer['title'],
                "color": 3447003,  # Blue
                "fields": [
                    {
                        "name": "💰 Cena",
                        "value": f"{offer['price']:,} PLN" if offer['price'] else "Negocjacyjnie",
                        "inline": True
                    },
                    {
                        "name": "📅 Rok",
                        "value": str(offer['year']) if offer['year'] else "N/A",
                        "inline": True
                    },
                    {
                        "name": "🏎️ Przebieg",
                        "value": f"{offer['mileage']:,} km" if offer['mileage'] else "N/A",
                        "inline": True
                    },
                    {
                        "name": "📍 Lokalizacja",
                        "value": offer['location'] if offer['location'] else "N/A",
                        "inline": True
                    },
                    {
                        "name": "⭐ Score",
                        "value": str(offer['score']),
                        "inline": True
                    },
                    {
                        "name": "🔗 Link",
                        "value": f"[Przejdź do oferty]({offer['url']})",
                        "inline": False
                    }
                ]
            }
            
            payload = {
                "embeds": [embed]
            }
            
            response = requests.post(
                DISCORD_WEBHOOK_URL,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 204:
                print(f"✅ Discord notification sent for: {offer['title']}")
                return True
            else:
                print(f"❌ Discord notification failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending Discord notification: {e}")
            return False
