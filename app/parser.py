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
            
            # Filter out: Seria 1
            if 'seria 1' in data['title'].lower() or data['title'].lower().startswith('bmw 1'):
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
            
            # Skip if price > 10000 PLN
            if data['price'] and data['price'] > 10000:
                return None
            
            # URL from first link
            link = article.find('a', href=re.compile(r'/osobowe/oferta/'))
            data['url'] = link.get('href') if link else None
            
            # Image URL from img tag
            img_tag = article.find('img')
            data['image_url'] = img_tag.get('src') if img_tag else None
            
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
            
            # Fuel type: "fuel_typeBenzynagearbox" pattern - stop at "gearbox"
            fuel_match = re.search(r'fuel_type([A-Za-z]+?)gearbox', text)
            data['fuel_type'] = fuel_match.group(1) if fuel_match else None
            
            # Engine capacity: "1995 cm3" or "2000cm3" etc - NOT "Seria X1991 cm3"
            # First remove the title part to avoid "Seria 51991 cm3"
            title_removed = text.replace(data['title'], '')
            capacity_match = re.search(r'(?<![A-Za-z0-9])(\d{3,4})\s*cm3', title_removed)
            if capacity_match:
                try:
                    cap = int(capacity_match.group(1))
                    # Valid engine capacities are typically 500-5000 cm3
                    if 500 <= cap <= 5000:
                        data['engine_capacity'] = cap
                    else:
                        data['engine_capacity'] = None
                except ValueError:
                    data['engine_capacity'] = None
            else:
                data['engine_capacity'] = None
            
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
