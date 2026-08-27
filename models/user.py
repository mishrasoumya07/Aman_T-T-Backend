from mongoengine import Document, StringField, EmailField

# User class Document ko inherit kar rahi hai. 
# Iska matlab ye MongoDB me ek 'table' (jise collection kehte hain) banegi.
class User(Document):
    
    # full_name text format me hoga
    full_name = StringField(
        required=True,       # Ye field khali nahi chhod sakte (Mandatory)
        max_length=100      
    )
    
    # email field automatically check karega ki email ka format sahi hai ya nahi
    email = EmailField(
        required=True,       # Email dena mandatory hai
        unique=True          # Duplicate allowed nahi hai (Ek email se 2 account nahi banenge)
    )
    
    # phone number text format me hai
    phone = StringField(
        required=True,       # Phone number dena mandatory hai
        unique=True,         # Duplicate phone number allowed nahi hai
        max_length=10        # Exact 10 digits tak hi limit set ki hai
    )
    
    # password text format me hoga
    password = StringField(
        required=True        # Password dena mandatory hai
    )
    
    # meta dictionary database ki settings batati hai
    meta = {
        "collection": "users" # MongoDB me is data ko 'users' naam ke folder(collection) me save karo
    }