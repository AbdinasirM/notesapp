from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Jtoken.generatejwt import generate_token
from Jtoken.verify import verify_token
from hashing.hash_salt_password import hash_password, generate_salt
from hashing.verifypassword import verify_password
from db.models.user_model import User
from db.operations.user.create import createUser
from db.operations.user.finduser import find_user 

# Initialize the API router with prefix and tags for user management
router = APIRouter(
    prefix="/api/v1/user",
    tags=["User"]  # Categorize these endpoints under "User" in the API docs
)

# Request model for user sign-in
class SignInRequest(BaseModel):
    email: str
    password: str

# Request model for token verification
class TokenVerification(BaseModel):
    token: str

@router.post("/signup")
async def sign_up(user: User):
    """
    Endpoint to register a new user.

    - Accepts user details as input.
    - Hashes the password with a salt.
    - Stores the user in the database.
    - Returns a JWT token upon successful registration.
    """
    try:
        # Generate a salt and hash the user's password
        salt = generate_salt()
        hashed_password = hash_password(user.password, salt)

        # Prepare the user data to store in the database
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": hashed_password,
            "salt": salt.decode('utf-8'),  # Store salt as a string for future use
            "notes": []  # Initialize with an empty notes list
        }

        # Save the user data to the database
        result = createUser(user_data)
        if not result:
            # Handle failure in user creation
            raise HTTPException(status_code=500, detail="Failed to create user.")

        # Extract the user ID from the database result
        user_id = result["_id"]

        # Generate a JWT token for the new user
        generated_token = generate_token({"user_id": str(user_id)})

        # Return a success response with the token
        return {
            "message": f"Hi {user.first_name}, welcome!",
            "token": generated_token,
        }

    except HTTPException as e:
        # Re-raise HTTP exceptions to return structured errors
        raise e
    except Exception as e:
        # Handle unexpected exceptions
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.post("/signin")
async def sign_in(request: SignInRequest):
    """
    Endpoint to authenticate an existing user.

    - Validates the user's email and password.
    - Generates a JWT token upon successful authentication.
    """
    try:
        # Retrieve user data from the database by email
        user_data = find_user(request.email)
        
        if not user_data or not isinstance(user_data, dict):
            # Return error if user is not found or data is invalid
            raise HTTPException(status_code=400, detail="Invalid email or password.")
        
        # Debugging: Uncomment to inspect retrieved user data
        # print(f"user_data: {user_data}")

        # Convert ObjectId to string for JSON compatibility
        user_data["_id"] = str(user_data["_id"])

        # Extract necessary fields from user_data
        user_id = user_data["_id"]
        salt = user_data["salt"]
        stored_password = user_data["password"]

        # Decode the stored salt back to bytes
        salt_bytes = salt.encode('utf-8')

        # Verify the user's provided password against the stored password
        if not verify_password(request.password, stored_password, salt_bytes):
            raise HTTPException(status_code=400, detail="Invalid email or password.")

        # Generate a JWT token for the authenticated user
        generated_token = generate_token({"user_id": user_id})

        # Return a success response with the token
        return {
            "message": f"Welcome back {user_data['first_name']}!",
            "token": generated_token
        }

    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        # Handle unexpected exceptions
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.post("/auth_verification")
async def verify_authentication(token_data: TokenVerification):
    """
    Endpoint to verify the validity of a JWT token.

    - Decodes the token to check if it is valid.
    - Returns the decoded token data if valid.
    """
    try:
        # Decode and verify the provided token
        decoded_data = verify_token(token_data.token)
        return {"message": "Token is valid", "data": decoded_data}

    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        # Handle unexpected exceptions
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
