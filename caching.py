import time

CACHE_DURATION = 3600  # 1 hour in seconds

_cache = {}  # { game_id: {"timestamp": float, "payload": dict} }

def get_cached_data(game_id):
    """
    Returns cached payload if it exists and hasn't expired, otherwise None.
    """
    entry = _cache.get(game_id)
    if not entry:
        return None

    if time.time() - entry["timestamp"] > CACHE_DURATION:
        del _cache[game_id]
        print(f"Cache expired for {game_id}")
        return None

    print(f"Serving {game_id} from cache")
    return entry["payload"]

def save_to_cache(game_id, payload):
    """
    Saves payload dict to the in-memory cache with the current timestamp.
    """
    _cache[game_id] = {"timestamp": time.time(), "payload": payload}
    print(f"Saved {game_id} to cache")
