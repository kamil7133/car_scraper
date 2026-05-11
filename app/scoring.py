class Scoring:
    @staticmethod
    def score_offer(offer):
        """Calculate score for an offer based on various criteria"""
        score = 0
        
        title = offer.get('title', '').lower()
        price = offer.get('price', 0) or 0
        year = offer.get('year', 0) or 0
        mileage = offer.get('mileage', 0) or 0
        
        # Model variant scoring
        if '330' in title:
            score += 40
        elif '328' in title:
            score += 30
        elif '325' in title:
            score += 20
        elif '320' in title:
            score += 10
        
        # Body type scoring
        if 'coupe' in title:
            score += 20
        elif 'sedan' in title:
            score += 10
        
        # Transmission
        if 'manualna' in title or 'manual' in title:
            score += 15
        
        # Price scoring (lower is better)
        if price > 0:
            if price < 5000:
                score += 30
            elif price < 8000:
                score += 20
            elif price < 12000:
                score += 10
        
        # Year scoring
        if year > 0:
            if year >= 2005:
                score += 20
            elif year >= 2000:
                score += 10
        
        # Mileage scoring
        if mileage > 0:
            if mileage < 150000:
                score += 25
            elif mileage < 200000:
                score += 15
            elif mileage < 250000:
                score += 5
        
        # Package/features
        if 'sport' in title or 'm sport' in title:
            score += 15
        if 'm package' in title or 'm pakiet' in title:
            score += 15
        
        # Condition hints
        if 'zadbany' in title:
            score += 10
        if 'serwis' in title:
            score += 5
        
        return min(score, 100)  # Cap at 100
