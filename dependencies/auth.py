# ==========================================
# IMPORTS SECTION
# ==========================================
import os # Environment variables (.env) ko padhne ke liye
from fastapi import Depends, HTTPException, status # Dependencies aur Errors (HTTP 401) handle karne ke liye
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # Request header se 'Bearer Token' nikalne ke liye
from jose import jwt, JWTError # Token ko decode (khushiya kholna) aur verify karne ke liye
from models.user import User # Database se user ki details check karne ke liye

# FastAPI ka inbuilt tool jo request aate hi automatically header se token pakad lega
security = HTTPBearer()

# Secret key jo token ko verify karne mein kaam aayegi (agar .env mein nahi hai toh default string use hogi)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "this-is-secert-key-flask")

# Algorithm jo check karega ki token kis style mein lock hua tha
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


# ==========================================
# SECURITY GUARD (Dependency Function)
# ==========================================
async def get_current_user(
    # Depends(security) ka matlab hai ki API chalne se pehle ye token nikal kar layega
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Step 1: Credentials object se actual lambi token string nikalna
    token = credentials.credentials
    
    try:
        # Step 2: Token ko secret key se decode karna check karne ke liye ki ye asli hai ya nahi
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        
        # Step 3: Payload (decoded data) ke andar se user ki ID ('sub') nikalna
        user_id = payload.get("sub")
        
        # Agar token theek hai par usme user_id (sub) gayab hai, toh error throw kardo
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token not authorized"
            )
            
    # Agar token ke sath kisi ne ched-chad ki hai ya token ka time khtam ho gaya hai
    except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid or expired token"
            )
            
    # Step 4: Token bilkul sahi hai! Ab database mein check karo ki is ID ka user exist karta hai ya nahi
    user = User.objects(id=user_id).first()
    
    # Agar token banne ke baad user apna account delete kar chuka ho, toh error dedo
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found"
        )

    # Step 5: Sab pass ho gaya! Ab is validated user ki detail aage route ko de do
    return user