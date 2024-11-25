from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_401_UNAUTHORIZED
import jwt 
from Jtoken.verify import verify_token
from db.operations.note.find import find_all_document, find_note
from db.operations.note.add import add_note
from db.operations.note.update import update_note
from db.models.note_model import Note, Note_update_data
from db.operations.note.delete import delete_note, delete_notes

from uuid import UUID

# Create a new API router for note-related endpoints
router = APIRouter(
    prefix="/api/v1/user/notes",
    tags=["notes"]  # Tag used for grouping routes in documentation
)

# Initialize HTTPBearer for token-based authentication
security = HTTPBearer()

def verify_token_helper(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Helper function to verify and decode the JWT token.
    Ensures that the token is valid and not expired.
    """
    token = credentials.credentials  # Extract the JWT token from the Authorization header
    try:
        # Validate the token and decode user data
        user_data = verify_token(token)
        return user_data
    except jwt.ExpiredSignatureError:
        # Handle expired token
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        # Handle invalid token
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid token. Please provide a valid token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/all")
async def get_all_notes(user_data: dict = Depends(verify_token_helper)):
    """
    Retrieve all notes for the authenticated user.

    - Uses the verified token to extract the user_id.
    - Fetches all notes associated with the user_id.
    """
    user_id = str(user_data.get("user_id", {}))  # Extract user_id from token
    
    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid token structure: user_id not found."
        )
    
    # Fetch notes for the user from the database
    all_notes = find_all_document(user_id)
    
    return {
        "message": "Access granted!",
        "Notes": all_notes  # Return the list of notes
    }

@router.post("/add")
async def create_a_note(
    user_data: dict = Depends(verify_token_helper),
    note_data: Note = Body(...)
):
    """
    Create a new note for the authenticated user.

    - Validates the token to extract user_id.
    - Adds a new note to the database with the provided data.
    """
    user_id = str(user_data.get("user_id", {}))  # Extract user_id from token
    
    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid token structure: user_id not found."
        )
    
    # Convert the note data into a dictionary format
    note_dict = note_data.dict()
    
    try:
        # Add the note to the database
        note_id = add_note(user_id, note_dict)
    except ValueError as e:
        # Handle errors during note creation
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"message": "Note added successfully!", "note_id": str(note_id)}

@router.put("/update/{note_id}")
async def update_a_note(
    note_id: str,
    user_data: dict = Depends(verify_token_helper),
    update_data: Note_update_data = Body(...)
):
    """
    Update an existing note for the authenticated user.

    - Validates the token to extract user_id.
    - Updates the specified note with the provided data.
    """
    user_id = str(user_data.get("user_id", {}))  # Extract user_id from token
    
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid token structure: user_id not found.")
    
    # Convert the update data into a dictionary format
    note_update_data = update_data.dict()

    # Ensure at least one field is being updated
    if all(value is None for value in note_update_data.values()):
        raise HTTPException(status_code=400, detail="No valid fields provided for update.")

    try:
        # Update the note in the database
        result = update_note(user_id, note_id, note_update_data)
        if result.get("error"):
            # Handle update errors
            raise HTTPException(status_code=400, detail=result["message"])
        return {
            "message": result.get("message", "Note updated successfully!"),
            "note_id": note_id,
            "updated_note": result.get("updated_note", {}),
        }
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{note_id}")
async def delete_a_note(note_id: str, user_data: dict = Depends(verify_token_helper)):
    """
    Delete a specific note for the authenticated user.

    - Validates the token to extract user_id.
    - Deletes the note with the given note_id from the database.
    """
    # Debugging: Print user data structure
    print(f"user_data received: {user_data}")

    # Handle user data structure differences
    if isinstance(user_data, dict):
        user_id = str(user_data.get("user_id", {}))
    elif isinstance(user_data, str):
        user_id = user_data  # Assume the string is the user_id directly
    else:
        raise HTTPException(status_code=400, detail="Invalid token structure: unexpected data format.")

    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid token structure: user_id not found.")
    
    try:
        # Attempt to delete the note
        result = delete_note(user_id, note_id)
        
        if not result.get("success", False):
            # Handle cases where the note is not found or cannot be deleted
            raise HTTPException(status_code=404, detail="Note not found or could not be deleted.")

        return JSONResponse(
            status_code=200,
            content={"message": "Note deleted successfully!", "note_id": note_id},
        )
    except Exception as e:
        # Log unexpected errors
        print(f"Error while deleting note: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the note.")
