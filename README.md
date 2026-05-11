# BMW Offer Hunter - MVP

A Python agent that monitors BMW E46 offers on OTOMOTO in Lower Silesia region.

## Features

- ✅ Scrapes OTOMOTO for BMW E46 listings
- ✅ Incremental fetching (detects new offers only)
- ✅ SQLite database for persistence
- ✅ Basic scoring system
- ✅ Discord webhook notifications
- ✅ Runs automatically every 5 minutes

## Project Structure

```
bmw_offer_hunter/
├── app/
│   ├── main.py          # Main event loop
│   ├── scraper.py       # OTOMOTO scraper
│   ├── parser.py        # HTML parser
│   ├── database.py      # SQLite operations
│   ├── notifier.py      # Discord notifications
│   ├── scoring.py       # Offer scoring logic
│   └── config.py        # Configuration
├── data/
│   └── offers.db        # SQLite database
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
└── README.md           # This file
```

## Installation

### 1. Clone the repository

```bash
git clone <repo>
cd bmw_offer_hunter
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

Copy `.env.example` to `.env` and fill in your Discord webhook:

```bash
cp .env.example .env
```

Edit `.env`:
```
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
DB_PATH=data/offers.db
SCRAPE_INTERVAL_SECONDS=300
```

## Usage

### Start the hunter

```bash
python3 -m app.main
```

The agent will:
1. Fetch OTOMOTO page
2. Parse listings
3. Check for new offers (via unique ID)
4. Score each new offer
5. Send Discord notification
6. Save to database
7. Wait 5 minutes
8. Repeat

### View database

```bash
sqlite3 data/offers.db
SELECT * FROM offers ORDER BY created_at DESC;
```

## Configuration

Edit `app/config.py` to customize:

- **Region**: Currently Dolny Śląsk (ID 10)
- **Model**: Currently BMW E46
- **Interval**: Default 300 seconds (5 minutes)
- **Timeout**: Default 10 seconds for requests

## Scoring System

Points are awarded for:
- Model variant (330i = 40pts, 328i = 30pts, etc.)
- Body type (coupe = 20pts)
- Transmission (manual = 15pts)
- Price (lower = more points)
- Year (newer = more points)
- Mileage (lower = more points)
- Features (M Sport, M Package, etc.)

Max score: 100 points

## Discord Integration

The bot sends embeds with:
- Offer title
- Price
- Year
- Mileage
- Location
- Score (1-100)
- Direct link to offer

## Database Schema

```sql
CREATE TABLE offers (
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
);
```

## Environment Variables

- `DISCORD_WEBHOOK_URL`: Discord webhook for notifications
- `DB_PATH`: Path to SQLite database (default: `data/offers.db`)
- `SCRAPE_INTERVAL_SECONDS`: Interval between hunts (default: `300`)

## Stack

- **Python 3.7+**
- **requests**: HTTP client
- **beautifulsoup4**: HTML parsing
- **sqlite3**: Database (built-in)
- **python-dotenv**: Environment variable management

## Roadmap

### v1.0 (Current - MVP)
- ✅ OTOMOTO scraper
- ✅ BMW E46 + Dolny Śląsk
- ✅ Incremental fetching
- ✅ SQLite database
- ✅ Basic scoring
- ✅ Discord webhooks

### v2.0 (Planned)
- OLX support
- Multiple BMW models
- Word blacklist/whitelist
- Logging to file
- Retry handling
- Email notifications

### v3.0 (Future)
- Dashboard UI
- FastAPI REST API
- Telegram bot
- Market price analysis
- Charts/graphs
- AI-powered scoring
- Fraud detection

## Notes

- The bot respects OTOMOTO's robots.txt and uses proper User-Agent headers
- CloudFlare protection is handled with appropriate headers
- No authentication required
- ~70 listings fetched per run

## License

MIT

## Author

Built with ❤️ for BMW E46 hunters
