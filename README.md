# Steam Pulse API

![Version](https://img.shields.io/badge/version-1.2.0-blue.svg) ![Python](https://img.shields.io/badge/python-3.11+-yellow.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-0.129.0-green.svg) ![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

**Steam Pulse** is a REST API that provides real-time sentiment analysis for any game on the Steam store. It returns a sentiment score, a `BUY / WAIT / AVOID` verdict, and the top keywords from positive and negative reviews — distilled from real player reviews using NLP.

---

## Key Features

- **Sentiment Score (0–100):** Quantifies the current mood of the player base.
- **Verdict Engine:** Returns `BUY`, `WAIT`, or `AVOID` based on recent review trends.
- **Keyword Extraction:** Top words from positive and negative reviews (pros/cons).
- **Game Title:** Returns the official game name alongside the App ID.
- **Smart Caching:** In-memory cache with a 1-hour TTL keeps responses fast and avoids hammering Steam's servers.
- **Clean JSON output:** Ready to plug into dashboards, Discord bots, or any frontend.

---

## Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) — chosen for speed and automatic `/docs` UI
- **NLP:** `NLTK` / `VADER` — sentiment scoring and keyword extraction
- **HTTP:** `requests` — fetches reviews and game details from Steam's public API
- **Caching:** In-memory Python dict with timestamp-based TTL
- **Deployment:** [Render](https://render.com)

---

## Installation & Setup

### Prerequisites
- Python 3.10+
- `pip`

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/steam-pulse-api.git
cd steam-pulse-api
```

### 2. Create a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # macOS / Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the server
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
Interactive docs at `http://127.0.0.1:8000/docs`.

---

## API Reference

### Health Check

**`GET /`**

```json
{
  "status": "online",
  "message": "Steam Pulse API is running."
}
```

---

### Analyze a Game

**`GET /analyze/{game_id}`**

| Parameter | Type | Description |
|-----------|------|-------------|
| `game_id` | integer | Steam App ID (e.g. `1091500` for Cyberpunk 2077) |

**Example request:**
```bash
curl http://127.0.0.1:8000/analyze/1091500
```

**Example response:**
```json
{
  "game_id": 1091500,
  "title": "Cyberpunk 2077",
  "success": true,
  "cached": false,
  "data": {
    "verdict": "BUY",
    "sentiment_score": 88,
    "keywords": {
      "pros": ["story", "graphics", "world", "characters", "soundtrack"],
      "cons": ["bugs", "crashes", "performance", "police", "ai"]
    },
    "raw_avg_compound": 0.7234,
    "total_reviews_analyzed": 50,
    "positive_reviews": 42,
    "negative_reviews": 8
  }
}
```

**Verdict thresholds:**

| Score | Verdict |
|-------|---------|
| 75–100 | `BUY` |
| 41–74 | `WAIT` |
| 0–40 | `AVOID` |

---

## Roadmap

### Phase 1 — MVP (Complete)
- [x] Sentiment analysis with VADER
- [x] Fetch reviews from Steam's public API
- [x] BUY / WAIT / AVOID verdict engine
- [x] Keyword extraction (pros/cons)
- [x] Game title in response
- [x] In-memory caching

### Phase 2 — Enhanced Intelligence
- [ ] AI-generated summary (LLM) of why players like/dislike the game
- [ ] Historical tracking — sentiment trends over time
- [ ] Side-by-side comparison of two games

### Phase 3 — Monetization
- [ ] API key authentication
- [ ] Tiered usage limits (Free / Pro)
- [ ] Webhook alerts (e.g. notify when sentiment drops below a threshold)

---

## License

Distributed under the MIT License.

---

**Built by davidqm7**
