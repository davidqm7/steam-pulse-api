import json
import os
import time

CACHE_DIR = "cache"
CACHE_DURATION = 3600  # 1 hour in seconds

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

def get_cached_data(game_id):
    """
    Checks if valid cached data exists for the given game_id.
    Returns the data (dict) if valid, or None if expired/missing.
    """
    filepath = os.path.join(CACHE_DIR, f"{game_id}.json")
    
    if not os.path.exists(filepath):
        return None
    
    try:
        # Check file age
        file_age = time.time() - os.path.getmtime(filepath)
        if file_age > CACHE_DURATION:
            print(f"Cache expired for {game_id} (Age: {int(file_age)}s)")
            return None # Cache is too old
            
        with open(filepath, "r") as f:
            print(f"Serving {game_id} from cache ⚡")
            return json.load(f)
            
    except Exception as e:
        print(f"Cache read error: {e}")
        return None

def save_to_cache(game_id, data):
    """
    Saves the analysis data to a JSON file.
    """
    filepath = os.path.join(CACHE_DIR, f"{game_id}.json")
    try:
        with open(filepath, "w") as f:
            json.dump(data, f)
        print(f"Saved {game_id} to cache 💾")
    except Exception as e:
        print(f"Cache write error: {e}")