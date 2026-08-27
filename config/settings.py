import os
from dotenv import load_dotenv

# Ye line .env file ko read karti hai
load_dotenv()

# Variables ko read karke unko dusri files ke liye available karwa rahe hain
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB", "fastapi_db")