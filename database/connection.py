# mongoengine library se connect function ko import kar rahe hain. 
# Yahi function actual database connection banata hai.
from mongoengine import connect

# Aapki banayi hui config/settings.py file se hum database ka naam 
# (MONGODB_DB) aur connection URL (MONGODB_URI) import kar rahe hain.
from config.settings import MONGODB_DB , MONGODB_URI

# Ye ek custom function banaya gaya hai jisko hum main.py mein call karenge.
def connect_database():
    # connect() function mein hum apna database name aur URL pass kar rahe hain.
    # Jaise hi ye line chalegi, FastAPI app MongoDB Atlas se jud jayega.
    connect(db=MONGODB_DB, host=MONGODB_URI)
    
    # Aap chaho toh yahan ek print statement add kar sakte ho test karne ke liye:
    # print("MongoDB Atlas via MongoEngine connected successfully!")