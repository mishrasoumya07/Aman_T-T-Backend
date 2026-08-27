# FastAPI framework se FastAPI class ko import kar rahe hain. 
from fastapi import FastAPI

# Humne jo custom function banaya tha 'database/connection.py' mein, usko yahan import kar rahe hain.
from database.connection import connect_database

# Apne auth wale router ko yahan import kar rahe hain
from routes.auth import router as auth_router

# Apne destination wale router ko yahan import kar rahe hain
from routes.destination import router as destination_router

# Yahan hum FastAPI ka ek instance (object) bana rahe hain jiska naam 'app' rakha hai.
app = FastAPI()

# FastAPI ko batayein ki auth wale routes ko app mein shamil karo
app.include_router(auth_router)

# FastAPI ko batayein ki destination wale routes ko bhi app mein shamil karo
app.include_router(destination_router)

# @app.on_event("startup") ek special decorator hai. 
@app.on_event("startup")
async def startup_event():
    # Terminal mein ek message print karega taaki hume process ka status pata chale.
    print("MongoDB Atlas se connect ho raha hai...")
    
    # Yahan hum apne database connection wale function ko call kar rahe hain. 
    connect_database()
    
    # Agar connection mein koi error nahi aaya aur wo successful raha, toh ye line chalegi.
    print("Database connected successfully!")

# @app.get("/") ek route decorator hai. 
@app.get("/")
async def root():
    # Ye function browser ko ek JSON dictionary return karega.
    return {"message": "FastAPI is running and MongoDB is connected!"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "mongodb": "Connected ✅"}