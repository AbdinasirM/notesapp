from bson import ObjectId  # Required to handle MongoDB ObjectId
from pymongo.errors import PyMongoError  # General MongoDB exception
from ...auth.auth_module import notes

def find_user(user_email: str):
    try:
        user = notes.find_one({"email": user_email})
        if user is None:
            return f"No user found with email: {user_email}"
        return user
    except PyMongoError as e:  # Catch any PyMongo-related errors
        return f"An error occurred while querying MongoDB: {e}"
        return None

# Test the function
# result = find_user("abdpi@example.com")
# print(result)
