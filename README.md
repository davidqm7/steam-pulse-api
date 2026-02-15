# Steam Pulse API 🎮

![Version](https://img.shields.io/badge/version-0.1.0-blue.svg) ![Python](https://img.shields.io/badge/python-3.11+-yellow.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg) ![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

**Steam Pulse** is a high-performance REST API designed for game developers, market analysts, and serious gamers. It provides real-time sentiment analysis, keyword extraction, and "Buy/Wait/Avoid" verdicts for any game on the Steam store.

Unlike standard scrapers that just return raw text, Steam Pulse uses advanced NLP (Natural Language Processing) to distill thousands of reviews into actionable data points, helping you understand *why* a game is succeeding or failing.

---

## 🚀 Key Features

* **Real-Time Sentiment Analysis:** Instantly gauge the mood of the player base with a 0-100 sentiment score.
* **"The Verdict" Engine:** Returns a clear `BUY`, `WAIT`, or `AVOID` recommendation based on recent review trends (e.g., detecting "review bombs" vs. genuine technical issues).
* **Keyword Extraction:** Automatically identifies the most common praises (e.g., "Soundtrack", "Story") and complaints (e.g., "Optimization", "Microtransactions").
* **Smart Caching:** Built-in caching layer to ensure fast response times for popular games and minimize load on Steam's servers.
* **JSON Output:** Clean, standardized JSON responses ready for integration into dashboards, Discord bots, or Excel sheets.

---

## 🛠️ Tech Stack

* **Core Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python) - chosen for its speed and automatic documentation.
* **Data Processing:** `Pandas` & `NLTK` / `VADER` - for efficient text analysis and sentiment scoring.
* **Scraping/Fetching:** `httpx` - for asynchronous HTTP requests to Steam's public storefront.
* **Caching:** `Redis` (Production) / In-Memory (Dev) - prevents redundant processing of the same game ID.
* **Deployment:** Dockerized for easy deployment on Render, Railway, or AWS.

---

## 📦 Installation & Setup

### Prerequisites
* Python 3.10 or higher
* `pip` (Python Package Manager)

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/steam-pulse-api.git](https://github.com/yourusername/steam-pulse-api.git)
cd steam-pulse-api
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Server
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

---

## 📖 API Reference

### 1. Health Check
Ensure the API is running.

* **Endpoint:** `GET /`
* **Response:**
    ```json
    {
      "status": "online",
      "message": "Steam Pulse API is running."
    }
    ```

### 2. Analyze a Game
Get the full sentiment report for a specific Steam Game ID.

* **Endpoint:** `GET /analyze/{game_id}`
* **Parameters:**
    * `game_id` (integer): The Steam App ID (e.g., `1091500` for Cyberpunk 2077).
* **Example Request:**
    ```bash
    curl [http://127.0.0.1:8000/analyze/1091500](http://127.0.0.1:8000/analyze/1091500)
    ```
* **Example Response:**
    ```json
    {
      "game_id": 1091500,
      "title": "Cyberpunk 2077",
      "verdict": "BUY",
      "sentiment_score": 88,
      "review_count_analyzed": 100,
      "keywords": {
        "pros": ["story", "graphics", "characters"],
        "cons": ["bugs", "police_system"]
      },
      "timestamp": "2024-05-20T14:30:00Z"
    }
    ```

---

## 🗺️ Roadmap

### Phase 1: MVP (Current)
- [x] Basic sentiment analysis using VADER.
- [x] Fetching reviews via Steam public API.
- [x] Simple caching to prevent rate limits.

### Phase 2: Enhanced Intelligence (Coming Soon)
- [ ] **AI Summarization:** Integrate LLMs (Gemini/GPT-4) to write a 2-sentence summary of *why* people like/dislike the game.
- [ ] **Historical Tracking:** Database integration to track sentiment trends over time (e.g., "Did the patch fix the review score?").
- [ ] **Competitor Comparison:** Endpoint to compare two game IDs side-by-side.

### Phase 3: Monetization
- [ ] API Key authentication via API Gateway.
- [ ] Tiered usage limits (Free vs. Pro).
- [ ] Webhook support for alerts (e.g., "Notify me if sentiment drops below 50%").

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Built by davidqm7**