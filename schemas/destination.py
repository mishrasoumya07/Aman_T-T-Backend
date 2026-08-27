# Pydantic se BaseModel import kar rahe hain, jo data format ko check (validate) karta hai
from pydantic import BaseModel

# =========================================================
# 1. CREATE SCHEMA (Nayi Destination add karne ke liye)
# =========================================================
# Ye tab use hoga jab frontend se naya data aayega (POST request).
# Isme 'id' nahi hai kyunki MongoDB save hone ke baad 'id' khud banata hai.
class DestinationCreate(BaseModel):
    name: str
    location: str
    description: str
    price: float
    duration: int
    image: str
    # Agar user koi activity nahi dalta, toh automatically ek khali list [] set ho jayegi
    activities: list[str] = [] 
    
# =========================================================
# 2. RESPONSE SCHEMA (Data wapas bhejne ke liye)
# =========================================================
# Ye tab use hoga jab hum backend se data frontend ko bhejenge (GET request).
class DestinationResponse(BaseModel):
    id: str  # Yahan 'id' dena zaroori hai taaki frontend ko pata chale ki konsi trip hai
    name: str
    location: str
    description: str
    price: float
    duration: int
    image: str
    activities: list[str]