from pydantic import BaseModel, EmailStr #datavalidation #dataparsing

class UserRegister(BaseModel):#basemodel-checks the data
    full_name: str
    email: EmailStr
    phone: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str