import time
import json
import random

class MockRedis:
    """Simulates Redis dictionary behavior with TTL"""
    def __init__(self):
        self.store = {}
        
    def get(self, key):
        if key in self.store:
            # Check TTL
            val, expiry = self.store[key]
            if time.time() > expiry:
                del self.store[key]
                print(f"      [Redis] Key {key} expired.")
                return None
            return val
        return None
        
    def setex(self, key, seconds, value):
        self.store[key] = (value, time.time() + seconds)
        print(f"      [Redis] SETEX {key} (TTL: {seconds}s)")

class MockDatabase:
    """Simulates a slow database"""
    def get_user(self, user_id):
        print(f"      [Database] SELECT * FROM users WHERE id = {user_id} ... (Slow)")
        time.sleep(1) # Simulate Latency
        return {"id": user_id, "name": "Alice", "plan": "Premium"}

# --- The Pattern Implementation ---

def get_user_profile(user_id, cache, db):
    key = f"user:{user_id}"
    
    # 1. Look Aside (Check Cache)
    cached_val = cache.get(key)
    if cached_val:
        print(f"   ✅ Cache HIT: {cached_val} (Latency: <1ms)")
        return json.loads(cached_val)
        
    print("   ❌ Cache MISS")
    
    # 2. Fetch from DB (Slow)
    start = time.time()
    data = db.get_user(user_id)
    duration = time.time() - start
    
    # 3. Write Back to Cache (with TTL of 60s)
    if data:
        cache.setex(key, 60, json.dumps(data))
        
    print(f"   Fetched from DB: {data} (Latency: {duration:.2f}s)")
    return data

def main():
    cache = MockRedis()
    db = MockDatabase()
    user_id = 101
    
    print("\n--- Request 1: First Visit (Cold Cache) ---")
    get_user_profile(user_id, cache, db)
    
    print("\n--- Request 2: Refresh Page (Warm Cache) ---")
    get_user_profile(user_id, cache, db)
    
    print("\n--- Request 3: Another User (Cold Cache) ---")
    get_user_profile(102, cache, db)

if __name__ == "__main__":
    main()
