import os
import redis
import json


REDIS_URL = os.getenv("REDIS_URL")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

if REDIS_URL:

    r = redis.from_url(REDIS_URL, decode_responses=True)
else:

    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

try:
    r.ping()
    print("✅ Redis connecté :", REDIS_URL or f"{REDIS_HOST}:{REDIS_PORT}")
except Exception as e:
    print("❌ Redis non disponible :", e)
def get_cache(key:str):
    try:
        data = r.get(f"v2:{key}")
        if data : 
            print(f"⚡ Cache HIT pour : {key}")
            return json.loads(data) if data else None
        print(f"ℹ️ Cache MISS pour : {key}")
    except Exception as e:
        print(f"❌ Erreur CRITIQUE get_cache : {e}")
        return None
    
def set_cache(key:str, value:dict, ttl: int =3600):
    try:
        print(f"DEBUG: Tentative d'écriture dans Redis - Clé: {key}")
        r.setex(f"v2:{key}", ttl, json.dumps(value))
    except Exception as e:
        print(f"❌ Erreur CRITIQUE set_cache : {e}")

RATE_LIMIT = 60
WINDOW = 60  # 60 req / minute

def is_rate_limited(ip: str):
    key = f"v2:rate:{ip}"

    try:
        current = r.incr(key)

        if current == 1:
            r.expire(key, WINDOW)

        if current > RATE_LIMIT:
            return True

        return False

    except Exception:
        return False