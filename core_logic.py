import requests
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import string
import statistics

# --- SETUP ---
# Download necessary NLTK data (run once)
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
    nltk.data.find('corpora/stopwords.zip')
    nltk.data.find('tokenizers/punkt.zip')
    nltk.data.find('tokenizers/punkt_tab.zip') 
except LookupError:
    print("Downloading NLTK data...")
    nltk.download('vader_lexicon')
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('punkt_tab')

# Define words to ignore (Standard English + Game-specific filler)
try:
    STOP_WORDS = set(stopwords.words('english'))
except:
    nltk.download('stopwords')
    STOP_WORDS = set(stopwords.words('english'))

GAME_STOP_WORDS = {
    "game", "play", "played", "playing", "hours", "time", "review", 
    "steam", "get", "like", "recommend", "fun", "good", "bad", "really",
    "make", "would", "much", "even", "story", "people", "games", "one", "buy",
    "best", "better", "great", "well", "lot", "feel", "feels", "still", "cant"
}
# Combine them
ALL_STOP_WORDS = STOP_WORDS.union(GAME_STOP_WORDS)

def fetch_game_title(game_id):
    """
    Fetches the game title from the Steam store API.
    """
    url = f"https://store.steampowered.com/api/appdetails?appids={game_id}"
    try:
        response = requests.get(url, headers={'User-Agent': 'SteamPulseAPI/0.1'})
        response.raise_for_status()
        data = response.json()
        if data[str(game_id)]['success']:
            return data[str(game_id)]['data']['name']
        return None
    except Exception as e:
        print(f"Error fetching title: {e}")
        return None

def fetch_reviews(game_id, num_reviews=50):
    """
    Fetches the most recent 'helpful' reviews from a Steam App ID.
    """
    url = f"https://store.steampowered.com/appreviews/{game_id}?json=1"
    
    params = {
        'filter': 'updated',       # Get recently updated reviews
        'language': 'english',     # Only English reviews
        'num_per_page': num_reviews,
        'purchase_type': 'all'     # Steam purchases + Key activations
    }
    
    headers = {
        'User-Agent': 'SteamPulseAPI/0.1' 
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data['success'] == 1 and data['query_summary']['total_reviews'] > 0:
            return data['reviews']
        else:
            return []
            
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return []

def extract_top_keywords(text_list):
    """
    Takes a list of strings, cleans them, and finds the top 5 keywords.
    """
    if not text_list:
        return []

    # 1. Combine all text into one giant string (lowercase)
    full_text = " ".join(text_list).lower()
    
    # 2. Remove punctuation
    full_text = full_text.translate(str.maketrans('', '', string.punctuation))
    
    # 3. Split into individual words
    tokens = word_tokenize(full_text)
    
    # 4. Filter out stop words and short words
    clean_tokens = [
        word for word in tokens 
        if word not in ALL_STOP_WORDS and len(word) > 2 and word.isalpha()
    ]
    
    # 5. Count frequency
    freq = FreqDist(clean_tokens)
    
    # 6. Return top 5 most common words
    return [word for word, count in freq.most_common(5)]

def analyze_sentiment(reviews):
    """
    Analyzes sentiment AND extracts keywords for Pros/Cons.
    """
    sia = SentimentIntensityAnalyzer()
    
    scores = []
    positive_count = 0
    negative_count = 0
    
    # Buckets for text to find keywords later
    pos_reviews_text = []
    neg_reviews_text = []

    for review in reviews:
        text = review['review']
        sentiment = sia.polarity_scores(text)
        compound_score = sentiment['compound']
        scores.append(compound_score)
        
        # Categorize and save text for keyword extraction
        # We use a slight buffer (0.05) to ignore purely neutral statements
        if compound_score >= 0.05:
            positive_count += 1
            pos_reviews_text.append(text)
        elif compound_score <= -0.05:
            negative_count += 1
            neg_reviews_text.append(text)
            
    if not scores:
        return {"error": "No reviews to analyze"}

    avg_score = statistics.mean(scores)
    # Normalize score to 0-100 scale
    normalized_score = int((avg_score + 1) * 50)

    # Determine Verdict
    if normalized_score >= 75:
        verdict = "BUY"
    elif normalized_score <= 40:
        verdict = "AVOID"
    else:
        verdict = "WAIT"

    # --- Extract Keywords ---
    top_pros = extract_top_keywords(pos_reviews_text)
    top_cons = extract_top_keywords(neg_reviews_text)

    return {
        "verdict": verdict,
        "sentiment_score": normalized_score,
        "keywords": {
            "pros": top_pros,
            "cons": top_cons
        },
        "raw_avg_compound": round(avg_score, 3),
        "total_reviews_analyzed": len(reviews),
        "positive_reviews": positive_count,
        "negative_reviews": negative_count
    }

# --- TEST RUNNER ---
if __name__ == "__main__":
    TEST_GAME_ID = 1091500 # Cyberpunk 2077
    print(f"--- Testing Steam Pulse Logic for Game ID: {TEST_GAME_ID} ---")
    reviews = fetch_reviews(TEST_GAME_ID, num_reviews=50)
    if reviews:
        result = analyze_sentiment(reviews)
        print("\n--- RESULTS ---")
        print(f"Verdict: {result['verdict']}")
        print(f"Score:   {result['sentiment_score']}/100")
        print(f"Pros:    {result['keywords']['pros']}")
        print(f"Cons:    {result['keywords']['cons']}")
    else:
        print("Failed to get reviews.")