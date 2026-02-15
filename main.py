from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Import your modules
import core_logic
import caching

app = FastAPI(
    title="Steam Pulse API",
    description="Real-time sentiment analysis for Steam games.",
    version="1.2.0"
)

# --- CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATA MODELS ---
class Keywords(BaseModel):
    pros: List[str]
    cons: List[str]

class SentimentAnalysis(BaseModel):
    verdict: str
    sentiment_score: int
    keywords: Keywords
    raw_avg_compound: float
    total_reviews_analyzed: int
    positive_reviews: int
    negative_reviews: int

class GameResponse(BaseModel):
    game_id: int
    success: bool
    cached: bool
    data: Optional[SentimentAnalysis] = None
    error: Optional[str] = None

# --- ENDPOINTS ---

@app.get("/")
def home():
    """Health check endpoint."""
    return {"status": "online", "message": "Steam Pulse API is running."}

@app.get("/analyze/{game_id}", response_model=GameResponse)
def analyze_game(game_id: int):
    """
    Analyzes the sentiment of a Steam game.
    Checks cache first to avoid rate limits.
    """
    # 1. CHECK CACHE FIRST
    cached_data = caching.get_cached_data(game_id)
    if cached_data:
        return {
            "game_id": game_id,
            "success": True,
            "cached": True,
            "data": cached_data
        }

    # 2. IF NOT IN CACHE, FETCH FROM STEAM
    print(f"Fetching fresh data for {game_id}...")
    reviews = core_logic.fetch_reviews(game_id, num_reviews=50)
    
    if not reviews:
        return {
            "game_id": game_id,
            "success": False,
            "cached": False,
            "error": "Game not found or no reviews available."
        }
    
    # 3. ANALYZE
    analysis = core_logic.analyze_sentiment(reviews)
    
    # 4. SAVE TO CACHE
    caching.save_to_cache(game_id, analysis)
    
    # 5. RETURN RESPONSE
    return {
        "game_id": game_id,
        "success": True,
        "cached": False,
        "data": analysis
    }