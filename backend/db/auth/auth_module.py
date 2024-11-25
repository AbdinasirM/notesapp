from dotenv import load_dotenv
import os
from pymongo import MongoClient

# Locate the .env file relative to the project root
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'auth/.env')

load_dotenv(dotenv_path)
secret_token = os.getenv("TOKEN")

# Test if variables are loaded
host = os.getenv("HOST")
port = os.getenv("PORT")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
auth_database = os.getenv("AUTH_DATABASE")


connection_flag = False
# print(f"Host: {host}, Port: {port}, Username: {username}, Password: {password}, Auth DB: {auth_database}")

client = MongoClient(
    host=host,
    port=27017,
    username=username,
    password=password,
    authSource=auth_database
)

notes = None

try:
    if client:
        connection_flag = True
        notesDB = client["newnotes"]
        notes = notesDB["notesCollection"]
        
    else:
        print("Database connection issue")
except Exception as e:
    print(f"Database connection error: {e}")

# Make sure notes is defined even if there's an error
if notes is None:
    print("Warning: notes collection is not initialized")
