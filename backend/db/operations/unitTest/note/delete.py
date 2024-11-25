from ...operations.note.delete import delete_note, delete_notes
from ..test_utils import log_test_result

def test_delete_notes():
    print("\n📝 Test: Delete Notes")
    print("======================")
    try:
        description = "should delete all notes for a user"
        user_id = "673e48b095834195c776cd2a"
        result = delete_notes(user_id)

        if result.get("success", False):  # Assuming a 'success' field in the response
            log_test_result(description, True)
        else:
            log_test_result(description, False, "Failed to delete all notes.")
    except Exception as e:
        log_test_result(description, False, e)

def test_delete_single_note(note_id):
    print("\n📝 Test: Delete Single Note")
    print("===========================")
    try:
        description = f"should delete note with ID {note_id}"
        user_id = "673e48b095834195c776cd2a"
        result = delete_note(user_id, note_id)

        if result.get("success", False):  # Assuming a 'success' field in the response
            log_test_result(description, True)
            print(f"   Deleted Note ID: {note_id}")
        else:
            log_test_result(description, False, "Failed to delete the note.")
    except Exception as e:
        log_test_result(description, False, e)


if __name__ == "__main__":
    note_id = "some-existing-note-id"  # Replace with a valid note_id or dynamically pass it
    test_delete_single_note(note_id)
