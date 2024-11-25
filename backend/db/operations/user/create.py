from ...auth.auth_module import notesDB, notes
from ...models.user_model import User
from ...models.user_model import Note

from pydantic import ValidationError
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException

def createUser(user):
    try:
        # Validate and create a User instance
        user = User(**user)
        
        # Convert the User model to a dictionary for MongoDB
        user_dict = user.model_dump()
        
        # Insert into the database
        notes.insert_one(user_dict)
        
        # Retrieve and return the inserted user
        return notes.find_one({"email": user.email})
    
   
    except DuplicateKeyError:
        # Raise an HTTPException for duplicate email
        raise HTTPException(status_code=400, detail="A user with this email already exists.")
    
    except ValidationError as e:
        # Raise HTTPException for validation errors
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")


# # User creation data
# new_user_data = {
#     "first_name": "Abdi",
#     "last_name": "Mumin",
#     "email": "emaiil4@e.com",
#     "password": "uvnsndvoisdnv",
#     "notes": []  # Initialize with an empty list of notes
# }

# adduser = createUser(new_user_data)

# print(adduser)


