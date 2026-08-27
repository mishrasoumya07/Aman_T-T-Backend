# ==========================================
# IMPORTS KAA SECTION
# ==========================================
import os # Environment variables (.env) padhne ke liye
import bcrypt # Password ko encrypt (hash) karne ke liye
from datetime import datetime, timedelta, timezone # Token ki expiry (time) set karne ke liye
from jose import jwt # JWT (JSON Web Token) banane aur padhne ke liye
from dotenv import load_dotenv # .env file ko load karne wala tool

# Ye function aapki .env file ko dhundhega aur usme likhe variables ko load karega
load_dotenv()

# ==========================================
# SECRET KEYS & SETTINGS
# ==========================================
# Ye aapke token ko lock karne ki 'Chabi' hai (Isko .env se utha rahe hain)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# Ye algorithm batata hai ki token kis tarike se lock hoga (Default HS256 rakha hai)
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# Token kitni der tak valid rahega (Default 60 minutes set kiya hai)
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


# ==========================================
# 1. PASSWORD HASHING (Encrypt karna)
# ==========================================
def hash_password(password: str):
    # User ke normal password ko pehle 'utf-8' mein encode kiya
    # Fir 'gensalt()' se usme kuch random characters jode taaki wo aur safe ho jaye
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    
    # Encrypt hone ke baad usko wapas normal string format mein decode karke return kar diya
    return hashed.decode("utf-8")


# ==========================================
# 2. PASSWORD VERIFY (Check karna)
# ==========================================
def verify_password(plain_password: str, hashed_password: str):
    # Ye function check karta hai ki jo password user ne abhi dala hai (plain_password),
    # kya wo database wale encrypted password (hashed_password) se match karta hai ya nahi
    return bcrypt.checkpw(plain_password.encode("utf-8"),
                          hashed_password.encode("utf-8"))
    
    
# ==========================================
# 3. ACCESS TOKEN BANANA (Login ki chabi)
# ==========================================
def create_access_token(user_id: str):
    # Current time mein utne minutes jod do jitne der tak token chalana hai (Expiry time)
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Payload wo data hota hai jo token ke andar chhupa hota hai
    # 'sub' (subject) mein hum user_id rakh rahe hain aur 'exp' mein expiry time
    payload = {
        "sub": user_id,
        "exp": expire
    }
    
    # Final step: Payload, Secret Key aur Algorithm ko milakar ek token (lamba sa text) bana do
    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )