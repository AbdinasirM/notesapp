from bson import ObjectId  # Required to handle MongoDB ObjectId
from pydantic import ValidationError
from ...auth.auth_module import notes
from ...models.note_model import Note


def add_note(user_id, note_data):
    """
    Creates a new note and adds it to the user's notes array in the database.

    :param user_id: The user's ID (string)
    :param note_data: Dictionary containing the note details (e.g., title, content)
    :return: Success message with updated user data or an error message
    """
    try:
        # Validate and create a Note instance using Pydantic
        # Ensures that only valid fields are allowed in the note_data
        note = Note(**note_data)
        
        # Convert the Note model to a dictionary
        # Ensures that the UUID field is converted to a string for storage in MongoDB
        note_dict = note.dict()

        # Validate that the user_id is a valid ObjectId
        if not ObjectId.is_valid(user_id):
            return {"error": "Invalid user_id format"}

        # Convert user_id to ObjectId for MongoDB queries
        user_id = ObjectId(user_id)

        # Check if the user exists in the database
        user = notes.find_one({"_id": user_id})
        if not user:
            # Return an error if the user does not exist
            return {"error": "User not found"}

        # Add the new note to the user's notes array using $push
        result = notes.update_one(
            {"_id": user_id},            # Filter to match the user by _id
            {"$push": {"notes": note_dict}}  # Add the new note to the notes array
        )

        if result.matched_count > 0:
            # Fetch the updated user document to confirm the note was added
            updated_user = notes.find_one({"_id": user_id})
            
            # Convert ObjectId to string for a more readable output
            updated_user["_id"] = str(updated_user["_id"])
            
            # Return success with the updated user data
            return {"success": f"Note added to user {user_id}", "user": updated_user}
        else:
            # If the update did not succeed, return an error
            return {"error": "User update failed"}
    
    except ValidationError as e:
        # Handle validation errors if the note_data does not conform to the Note model
        return {"error": str(e)}


# # Example note creation data
# new_note_data = {
#     "title": "journal note",        # Title of the note
#     "content": "so this is about"   # Content of the note
# }

# # Add the note to the user
# addnote = add_note("673e79c6ccd64dc0783f7081", new_note_data)

# # Print the result of the operation
# print(addnote)
