# ==========================================
# IMPORTS KAA SECTION
# ==========================================
# FastAPI ki zaroori cheezein import kar rahe hain (APIRouter routes banane ke liye, HTTPException errors ke liye, Depends security guard ke liye)
from fastapi import APIRouter, HTTPException, Depends

# Jo data user form mein daalega (jaise Email, Password), uska format schemas se aayega
from schemas.user import UserRegister, UserLogin

# Database (MongoDB) mein data save karne ka structure (Model) import kar rahe hain
from models.user import User

# Password ko safe rakhne (hash) aur check karne ke tools, aur Login Token banane ke tools
from utils.security import hash_password, verify_password, create_access_token

# MongoDB mein agar same email dobara aaye toh error pakadne ke liye NotUniqueError import kiya
from mongoengine.errors import NotUniqueError

# ==========================================
# ROUTER SETUP
# ==========================================
# Hum ek router bana rahe hain jiska 'prefix' /auth hai. 
# Iska matlab is file ke saare URLs ke aage automatically '/auth' lag jayega (jaise /auth/register).
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"] # Swagger UI mein ye routes 'Authentication' heading ke andar ek sath dikhenge
)

# ==========================================
# 1. REGISTER ROUTE (Naya Account Banane Ke Liye)
# ==========================================
@router.post("/register")
async def register(user: UserRegister):
    # User ne jo password dala hai, usko encrypt (hash) kar rahe hain taaki database mein safe rahe
    hashed_password = hash_password(user.password)
    
    # Naye user ki details ko database model ke hisaab se ek object mein daal rahe hain
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        password=hashed_password # Yahan encrypted password save ho raha hai
    )
    
    # Try block lagaya taaki agar error aaye toh server crash na ho
    try:
        # Data ko finally MongoDB database mein save kar rahe hain
        new_user.save()
        
        # Save hone ke baad frontend ko success message aur nayi user_id bhej rahe hain
        return {
            "message":"User Registered Successfully ✅",
            "User_id":str(new_user.id)
        }
    except NotUniqueError:
        # Agar duplicate email aata hai, toh 400 Bad Request ka error return karenge
        raise HTTPException(status_code=400, detail="This Email is already registered!")
    

# ==========================================
# 2. LOGIN ROUTE (Account Mein Entry Ke Liye)
# ==========================================
@router.post("/login")
async def login(user: UserLogin):
    # Step 1: Check kar rahe hain ki user ki email ID se koi account database mein hai ya nahi
    db_user = User.objects(email=user.email).first()
    
    # Agar email database mein nahi mila, toh 401 error message bhej do
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid Email or password")
    
    # Step 2: Email mil gaya, toh check karo ki user ne jo password dala hai wo match ho raha hai ya nahi
    password_valid = verify_password(user.password, db_user.password)
    
    # Agar password galat hai, toh wapas 401 error de do
    if not password_valid:
        raise HTTPException(status_code=401, detail="Invalid Email or password")
    
    # Step 3: Agar email aur password dono sahi hain, toh ek naya "Access Token" banao
    access_token = create_access_token(str(db_user.id))
    
    # Final Step: Frontend ko success message, lamba sa token, aur thodi basic details bhej do
    return {
        "message": "Login Successful ✅",
        "access_token": access_token,
        "full_name": db_user.full_name,
        "email": db_user.email,
        "token_type": "bearer" # Bearer batata hai ki ye token standard type ka hai
    }

# ==========================================
# 3. GET ALL USERS (Database se saare registered users dekhne ke liye)
# ==========================================
@router.get("/users")
async def get_all_users():
    # Database (MongoDB) se sabhi users ka sara data nikal lo
    users = User.objects.all()
    
    # Un sabhi users ko ek list mein pack karke return kar do
    # Dhyan rahe: Hum yahan password return nahi kar rahe taaki API secure rahe
    return [
        {
            "id": str(user.id),
            "full_name": user.full_name,
            "email": user.email,
            # Agar kisi user ka phone number database mein nahi hai, toh error na aaye, balki 'N/A' dikha de
            "phone": getattr(user, "phone", "N/A")
        }
        for user in users # Loop chala kar ek-ek user ko read kar rahe hain
    ]