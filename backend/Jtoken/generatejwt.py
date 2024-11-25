import jwt
import datetime
from dotenv import load_dotenv
import os

# Locate the .env file relative to the project root
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Jtoken/.env')

load_dotenv(dotenv_path)
secret_token = os.getenv("TOKEN")


# print(secret_token)

# Validate the secret token
if not secret_token:
    raise ValueError("TOKEN environment variable is not set or invalid.")

def generate_token(user_id):
    # If `user_id` is a dictionary, extract its actual ID
    if isinstance(user_id, dict) and "user_id" in user_id:
        user_id = user_id["user_id"]
    
    payload = {
        "user_id":user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30),
        "iat":datetime.datetime.now(datetime.timezone.utc) 
    }
    
    token = jwt.encode(payload, secret_token,algorithm="HS256")
    return token

# user_id = "43ff43"
# result = generate_token(user_id)

# print(result)
# #eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNDNmZjQzIiwiZXhwIjoxNzMyMjI3NjM0LCJpYXQiOjE3MzIyMjc0NTR9.iiiv7dKcOG-_a52Ccm-TJqb0I363N7IYyWLcCUg8Lx8