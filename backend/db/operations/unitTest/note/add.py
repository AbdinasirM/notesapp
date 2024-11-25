from ...operations.note.add import add_note
from ..test_utils import log_test_result

def test_create_note():
    print("\n📝 Test: Create Note")
    print("=====================")
    try:
        description = "should create a new note"
        user_id = "673e48b095834195c776cd2a"
        new_note_data = {
            "title": "journal note",
            "content": "so this is about"
        }
        result = add_note(user_id, new_note_data)

        if result.get("success", False):  # Assuming a 'success' field in the response
            note_id = result.get("note_id")  # Assuming the response contains 'note_id'
            log_test_result(description, True)
            print(f"   Created Note ID: {note_id}")
            return note_id  # Return the created note_id for use in other tests
        else:
            log_test_result(description, False, "Note creation failed.")
    except Exception as e:
        log_test_result(description, False, e)


if __name__ == "__main__":
    created_note_id = test_create_note()
