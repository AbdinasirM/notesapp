from ...operations.note.find import find_all_document, find_note
from ..test_utils import log_test_result

def test_find_all_notes():
    print("\n📝 Test: Find All Notes")
    print("========================")
    try:
        description = "should find all notes for a user"
        user_id = "673e48b095834195c776cd2a"
        result = find_all_document(user_id)

        if "error" not in result:
            log_test_result(description, True)
            print(f"   Notes Found: {result}")
        else:
            log_test_result(description, False, result["error"])
    except Exception as e:
        log_test_result(description, False, e)

def test_find_specific_note(note_id):
    print("\n📝 Test: Find Specific Note")
    print("===========================")
    try:
        description = f"should find note with ID {note_id}"
        user_id = "673e48b095834195c776cd2a"
        result = find_note(user_id, note_id)

        if "error" not in result:
            log_test_result(description, True)
            print(f"   Found Note Details: {result}")
        else:
            log_test_result(description, False, result["error"])
    except Exception as e:
        log_test_result(description, False, e)


if __name__ == "__main__":
    note_id = "some-existing-note-id"  # Replace with a valid note_id
    test_find_specific_note(note_id)
