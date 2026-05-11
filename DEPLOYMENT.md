# BMW Offer Hunter - MVP v1.0 Deployment Guide

## ✅ Status: READY FOR PRODUCTION

All components tested and working:
- ✅ Scraper (requests + BeautifulSoup4)
- ✅ Parser (HTML extraction)
- ✅ Database (SQLite persistence)
- ✅ Scoring system (1-100 points)
- ✅ Discord notifications (webhook ready)
- ✅ Main event loop (5-minute cycles)

## Quick Start

### 1. Prerequisites
- Python 3.7+
- `pip` package manager
- Discord server with webhook permissions (optional, but recommended)

### 2. Installation

```bash
# Navigate to project directory
cd bmw_offer_hunter

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Edit `.env` file:

```bash
# Get Discord webhook URL from:
# Server Settings > Integrations > Webhooks > Create Webhook
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN

# Database location (default is fine)
DB_PATH=data/offers.db

# Check interval in seconds (default 300 = 5 minutes)
SCRAPE_INTERVAL_SECONDS=300
```

### 4. Run the Agent

```bash
python3 -m app.main
```

You should see:
```
  ╔════════════════════════════════════════╗
  ║  🚗 BMW OFFER HUNTER - MVP v1.0       ║
  ║  Śląsk Edition                         ║
  ╚════════════════════════════════════════╝

Interval: 300 seconds
Database: data/offers.db

Press CTRL+C to stop
```

## Features Included

### Scraping
- ✅ Fetches OTOMOTO search results (~70 listings per hunt)
- ✅ Handles CloudFlare protection with proper User-Agent
- ✅ No API key needed
- ✅ Parses all key fields: ID, title, price, year, mileage, location, URL

### Data Processing
- ✅ **Incremental fetching**: Only processes new offers (via unique ID check)
- ✅ **Scoring**: Awards 1-100 points based on:
  - Model variant (330i = 40pts, etc.)
  - Body type (coupe bonus)
  - Price (lower = more points)
  - Year (newer = more points)
  - Mileage (lower = more points)
  - Features (M Sport, M Package)

### Storage
- ✅ **SQLite database** for persistent storage
- ✅ **Auto-created schema** on first run
- ✅ Tracks: ID, title, price, year, mileage, location, URL, score, timestamp

### Notifications
- ✅ **Discord embeds** with complete offer details
- ✅ Automatic formatting with colors
- ✅ Direct links to OTOMOTO listings
- ✅ Score display (helps filter quality offers)

### Automation
- ✅ **5-minute cycles** (configurable)
- ✅ **Graceful shutdown** (CTRL+C)
- ✅ **Persistent state** across restarts

## Monitoring

### View Recent Offers

```bash
# Open SQLite shell
sqlite3 data/offers.db

# List recent offers
SELECT title, price, year, mileage, score, created_at 
FROM offers 
ORDER BY created_at DESC 
LIMIT 10;

# Get statistics
SELECT COUNT(*) as total_offers, AVG(score) as avg_score FROM offers;

# Find high-scoring deals
SELECT title, price, score FROM offers WHERE score >= 80 ORDER BY score DESC;
```

### Check Logs

The agent prints to stdout:
- ✅ Hunt number and timestamp
- ✅ Number of articles found
- ✅ New offers detected
- ✅ Details of each new offer
- ✅ Database summary

## Deployment Options

### Option 1: Local Machine (Development)
```bash
python3 -m app.main
```
Keep terminal open. Stop with CTRL+C.

### Option 2: VPS/Server (Production Recommended)

#### Using `screen` (simple):
```bash
screen -S bmw-hunter
python3 -m app.main
# Detach: CTRL+A then D
# Reattach: screen -r bmw-hunter
```

#### Using `nohup` (fire and forget):
```bash
nohup python3 -m app.main > logs/hunter.log 2>&1 &
```

#### Using systemd (robust):
Create `/etc/systemd/system/bmw-hunter.service`:
```ini
[Unit]
Description=BMW Offer Hunter
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/bmw_offer_hunter
ExecStart=/path/to/.venv/bin/python3 -m app.main
Restart=on-failure
RestartSec=60

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable bmw-hunter
sudo systemctl start bmw-hunter
sudo systemctl status bmw-hunter
```

### Option 3: Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python3", "-m", "app.main"]
```

Build and run:
```bash
docker build -t bmw-hunter .
docker run -d -e DISCORD_WEBHOOK_URL="..." bmw-hunter
```

## Scoring Examples

### High Score (80-100)
- BMW 330i M Sport
- Manual transmission
- Cheap (<5000 PLN)
- Low mileage (<150k km)
- Recent year (2005+)

### Medium Score (50-79)
- BMW 320i or 328i
- Automatic transmission
- Mid-range price
- Moderate mileage (150-200k km)
- Decent year (2000+)

### Low Score (1-49)
- BMW 320 or lower
- High mileage (>250k km)
- Old year (<2000)
- High price

## Troubleshooting

### No offers being found
- Check that OTOMOTO is accessible: `curl "https://www.otomoto.pl/osobowe/bmw/e46/"`
- Check User-Agent in `app/config.py`
- OTOMOTO may have changed HTML structure

### Discord notifications not sending
- Verify webhook URL in `.env`
- Test webhook: 
  ```bash
  curl -X POST "WEBHOOK_URL" -H "Content-Type: application/json" -d '{"content":"test"}'
  ```

### Database locked error
- Close any other SQLite connections
- Delete `data/offers.db-journal` if it exists

### High CPU usage
- Increase `SCRAPE_INTERVAL_SECONDS` in `.env`
- Default is 300 seconds (5 minutes)

## Next Steps (v2.0+)

See main README.md for planned features:
- OLX support
- Multiple BMW models
- Keyword filtering
- Email notifications
- Dashboard UI
- Market analysis
- AI scoring

## Support

For issues:
1. Check `.env` is configured correctly
2. Verify internet connection
3. Check OTOMOTO website is accessible
4. Review stdout logs for errors

## License & Credits

Built with ❤️ for BMW E46 hunters.

---

**Happy hunting! 🏹🚗**
