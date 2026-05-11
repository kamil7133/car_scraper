import re

class Parser:
    @staticmethod
    def parse_offer(article):
        """Extract offer data from article element"""
        try:
            data = {}
            
            # ID from data attribute
            data['id'] = article.get('data-id')
            if not data['id']:
                return None
            
            # Title from h2
            title_h2 = article.find('h2')
            data['title'] = title_h2.get_text(strip=True) if title_h2 else None
            
            if not data['title']:
                return None
            
            # Price from h3
            price_h3 = article.find('h3')
            if price_h3:
                price_text = price_h3.get_text(strip=True)
                try:
                    data['price'] = int(price_text.replace(' ', '').replace(',', ''))
                except ValueError:
                    data['price'] = None
            else:
                data['price'] = None
            
            # URL from first link
            link = article.find('a', href=re.compile(r'/osobowe/oferta/'))
            data['url'] = link.get('href') if link else None
            
            # Extract details from text
            text = article.get_text()
            
            # Mileage: "mileage98 000 km" or "mileage98000km"
            mileage_match = re.search(r'mileage([\d\s]+)km', text)
            if mileage_match:
                try:
                    data['mileage'] = int(mileage_match.group(1).replace(' ', ''))
                except ValueError:
                    data['mileage'] = None
            else:
                data['mileage'] = None
            
            # Year: "year2019"
            year_match = re.search(r'year(\d{4})', text)
            if year_match:
                try:
                    data['year'] = int(year_match.group(1))
                except ValueError:
                    data['year'] = None
            else:
                data['year'] = None
            
            # Location: "Wrocław (Dolnośląskie)"
            location_match = re.search(r'([A-Z][a-ząćęłńóśźż\s]+?)\s*\(', text)
            if location_match:
                data['location'] = location_match.group(1).strip()
            else:
                data['location'] = None
            
            return data
        except Exception as e:
            print(f"❌ Error parsing offer: {e}")
            return None
