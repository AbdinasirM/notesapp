from bson import ObjectId  # Required to handle MongoDB ObjectId
from pydantic import ValidationError
from ...auth.auth_module import notes
from ...models.note_model import Note_update_data
from .find import find_note


def update_note(user_id, note_id, update_data):
    """
    Updates a specific note in the user's notes array.

    :param user_id: The user's ID (string)
    :param note_id: The ID of the note to update (string)
    :param update_data: Dictionary containing fields to update in the note
    :return: A success message with the updated note or an error message
    """
    try:
        # Validate the update_data against the Note_update_data Pydantic model
        # Ensures that only valid fields are passed for the update
        note_update_data = Note_update_data(**update_data)
    except ValidationError as e:
        # Return validation errors if update_data contains invalid fields
        return {"error": "Validation error", "details": e.errors()}
    
    # Find the note to ensure it exists
    note_to_update = find_note(user_id, note_id)
    if not note_to_update or isinstance(note_to_update, dict) and "error" in note_to_update:
        # Return an error if the note is not found
        return {"error": "Note not found", "details": note_to_update}
    
    # Prepare the update payload by including only non-None fields
    set_updates = {}
    for field, value in note_update_data.model_dump().items():
        if value is not None:  # Only include fields with non-None values
            set_updates[f"notes.$.{field}"] = value
    
    # MongoDB query to find the document with the matching user_id and note_id
    query = {"_id": ObjectId(user_id), "notes.id": note_id}
    
    # MongoDB update payload to set the updated fields
    update_payload = {"$set": set_updates}
    
    # Perform the update operation
    result = notes.update_one(query, update_payload)
    
    if result.modified_count > 0:
        # If the update was successful, merge the old note data with the updates and return success
        return {
            "success": True,
            "message": "Note updated successfully",
            "updated_note": {**note_to_update, **update_data},
        }
    else:
        # If no changes were made, return a message indicating no updates occurred
        return {"success": False, "message": "No note was updated. Data might already be up-to-date."}


# # Example usage
# try:
#     # Example user_id and note_id
#     user_id = "6743bc73eaa20ae4b350038b"
#     note_id = "ec178d85-0343-4f39-88df-bbceaa375b2a"
    
#     # Data to update the note
#     update_data = {
#         "content": "This is the updated content."  # Example update
#     }

#     # Call the update_note function and print the result
#     result = update_note(user_id, note_id, update_data)
#     print(result)
    
# except Exception as e:
#     # Print any unexpected errors
#     print(f"Error: {e}")

