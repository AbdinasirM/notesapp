import jwt
import datetime
from dotenv import load_dotenv
import os

# Locate the .env file relative to the project root
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Jtoken/.env')

load_dotenv(dotenv_path)
secret_token = os.getenv("TOKEN")

def verify_token(token):
    try:
        # Decode and verify the token
        decoded = jwt.decode(token, secret_token, algorithms="HS256")
        return decoded
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Token has expired")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Invalid token")


# token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNDNmZjQzIiwiZXhwIjoxNzMyNDE0NTc5LCJpYXQiOjE3MzI0MTQzOTl9.kj_IuHmRAHyufyLNMQFqtcgHi6UbkBFTGdFBhx2fiF4"
# verify = verify_token(token)
# print(verify)