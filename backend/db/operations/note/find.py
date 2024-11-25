from ...auth.auth_module import notes
from bson import ObjectId  # Required to handle MongoDB ObjectId
from uuid import UUID  # For validating UUID format


# def find_all_document(user_id):
#     """
#     Retrieves all documents for a specific user by user_id.

#     :param user_id: The user's ID (string)
#     :return: The user's document if found, or an error message
#     """
#     # Ensure user_id is a valid ObjectId
#     if not ObjectId.is_valid(user_id):
#         return {"error": "Invalid user_id format"}  # Return error for invalid ObjectId

#     # Convert user_id to ObjectId for MongoDB queries
#     user_id = ObjectId(user_id)
    
#     # Query the database for the user document
#     note = notes.find_one({"_id": user_id})
    
#     if not note:
#         # Return an error if the user document does not exist
#         return {"error": "User not found"}
    
#     # Return the entire user document
#     # return {"success": True, "user_document": note}
#     return note



def serialize_document(document):
    """
    Serializes a MongoDB document by converting ObjectId fields to strings.
    """
    if isinstance(document, dict):
        for key, value in document.items():
            if isinstance(value, ObjectId):
                document[key] = str(value)
    return document

def find_all_document(user_id):
    """
    Retrieves all documents for a specific user by user_id.

    :param user_id: The user's ID (string)
    :return: The user's document if found, or an error message
    """
    # Ensure user_id is a valid ObjectId
    if not ObjectId.is_valid(user_id):
        return {"error": "Invalid user_id format"}  # Return error for invalid ObjectId

    # Convert user_id to ObjectId for MongoDB queries
    user_id = ObjectId(user_id)
    
    # Query the database for the user document
    note = notes.find_one({"_id": user_id})
    
    if not note:
        # Return an error if the user document does not exist
        return {"error": "User not found"}
    
    # Serialize the document before returning
    serialized_note = serialize_document(note)
    
    # Return the serialized user document
    return {"success": True, "user_document": serialized_note}

def find_note(user_id, note_id):
    """
    Finds a specific note in a user's notes array.

    :param user_id: The user's ID (string)
    :param note_id: The ID of the note to find (UUID string)
    :return: The note if found, or an error message
    """
    # Ensure user_id is a valid ObjectId
    if not ObjectId.is_valid(user_id):
        return {"error": "Invalid user_id format"}  # Return error for invalid ObjectId
    
    # Convert user_id to ObjectId for MongoDB queries
    user_id = ObjectId(user_id)
    
    # Validate note_id is a valid UUID
    try:
        note_id = UUID(note_id)  # Converts string to UUID for validation
    except ValueError:
        return {"error": "Invalid note_id format"}  # Return error for invalid UUID
    
    # Query the database for the user document
    user_data = notes.find_one({"_id": user_id})
    
    if not user_data or "notes" not in user_data:
        # Return an error if the user document does not exist or has no notes
        return {"error": "User not found or no notes available"}
    
    # Search for the note in the user's notes array
    for note in user_data["notes"]:
        if note["id"] == str(note_id):  # Compare the note_id as a string
            return {"success": True, "note": note}  # Return the matching note
    
    # Return an error if the note was not found
    return {"error": "Note not found"}


# # Example Usage
# try:
#     # Find all documents for a user
#     result = find_all_document("673e48b095834195c776cd2a")
#     print(result)

#     # Uncomment to find a specific note
#     # result = find_note("673e48b095834195c776cd2a", "a7dff951-0317-4f10-94dd-2923a44932d4")
#     # print(result)

# except Exception as e:
#     # Print any unexpected errors
#     print(f"Error: {e}")
