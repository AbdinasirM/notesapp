from bson import ObjectId  # Required to handle MongoDB ObjectId
from ...auth.auth_module import notes
from .find import find_note

def delete_note(user_id, note_id):
    """
    Deletes a specific note from the user's notes array.

    :param user_id: The user's ID (as a string)
    :param note_id: The ID of the note to delete (as a string)
    :return: A success message or an error message
    """
    try:
        user_id = ObjectId(user_id)  # Ensure user_id is converted to ObjectId for MongoDB
    except Exception as e:
        return {"error": "Invalid user ID format", "details": str(e)}

    # Find the note to ensure it exists
    note_to_delete = find_note(user_id, note_id)
    if not note_to_delete or (isinstance(note_to_delete, dict) and "error" in note_to_delete):
        return {"error": "Note not found", "details": note_to_delete}

    # Use $pull to remove the specific note from the notes array
    result = notes.update_one(
        {"_id": user_id},  # Match the user's document by _id
        {"$pull": {"notes": {"id": note_id}}}  # Remove the note with matching id
    )

    if result.modified_count > 0:
        return {"success": True, "message": f"Note with ID {note_id} has been deleted successfully."}
    else:
        return {"error": "Failed to delete the note. It may not exist or is already deleted."}



def delete_notes(user_id):
    """
    Clears all notes from the user's notes array.

    :param user_id: The user's ID
    :return: A success message or an error message
    """
    user_id = ObjectId(user_id)
    
    # Use $set to clear the notes array
    result = notes.update_one(
        {"_id": user_id},  # Match the user's document by _id
        {"$set": {"notes": []}}  # Set the notes field to an empty list
    )
    
    if result.modified_count > 0:
        return f"All notes for user {user_id} have been deleted successfully."
    else:
        return {"error": "Failed to delete notes. User may not exist or already have an empty notes array."}


# # Example Usage
# try:
#     user_id = "673e48b095834195c776cd2a"
    
#     note_id = "a7dff951-0317-4f10-94dd-2923a44932d4"

#     # # Delete a single note
#     # result = delete_note(user_id, note_id)
#     # print(result)

#     # Optionally, delete all notes
#     result = delete_notes(user_id)
#     print(result)
    
# except Exception as e:
#     print(f"Error: {e}")
