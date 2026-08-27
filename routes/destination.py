from fastapi import APIRouter, Depends, status
from models.destination import Destination
from models.user import User
from schemas.destination import DestinationCreate, DestinationResponse

# Aapka Guard jo token check karega
from dependencies.auth import get_current_user

# Router setup (Swagger UI mein ye 'Destination' section banayega)
router = APIRouter(
    prefix="/destinations",
    tags=["Destination"]
)

# =========================================================
# 1. CREATE DESTINATION (POST) - 🔒 Lock Laga Hua Hai
# =========================================================
# Sirf login user hi naya package add kar sakta hai.
# Bug Fix: Yahan humne 'response_model=DestinationResponse' kar diya hai.
@router.post("/", response_model=DestinationResponse)
async def create_destination(
    destination: DestinationCreate, 
    current_user: User = Depends(get_current_user) # Is line ki wajah se Swagger mein Lock 🔒 aayega
):
    # Naya destination object banaya aur data set kiya
    new_destination = Destination(
        name=destination.name,
        location=destination.location,
        description=destination.description,
        price=destination.price,
        duration=destination.duration,
        image=destination.image,
        activities=destination.activities
    )
    
    # Naye destination ko MongoDB mein save kar diya
    new_destination.save()
    
    # Save hone ke baad wahi data (ID ke sath) wapas bhej diya
    return {
        "id": str(new_destination.id),
        "name": new_destination.name,
        "location": new_destination.location,
        "description": new_destination.description,
        "price": new_destination.price,
        "duration": new_destination.duration,
        "image": new_destination.image,
        "activities": new_destination.activities
    }
    
    
# =========================================================
# 2. GET ALL DESTINATIONS (GET) - 🔓 Khula Hua Hai
# =========================================================
# Ye route public hai (No Lock). Website ka koi bhi visitor saari trips dekh sakta hai.
@router.get("/", response_model=list[DestinationResponse])
async def get_destination():
    # Database se saari destinations nikal li
    destinations = Destination.objects.all()
    
    # List comprehension ka use karke sabhi ko ek list mein pack kiya
    return [
        {
            "id": str(destination.id),
            "name": destination.name,
            "location": destination.location,
            "description": destination.description,
            "price": destination.price,
            "duration": destination.duration,
            "image": destination.image,
            "activities": destination.activities
        }
        for destination in destinations   
    ]