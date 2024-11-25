from ...operations.note.update import update_note
from ..test_utils import log_test_result

def test_update_note():
    print("\n📝 Test: Update Note")
    print("=====================")
    try:
        description = "should update the content of an existing note"
        user_id = "673e48b095834195c776cd2a"
        note_id = "a7dff951-0317-4f10-94dd-2923a44932d4"
        update_data = {
            "content": "This is the updated content."
        }
        result = update_note(user_id, note_id, update_data)

        if result.get("success", False):  # Assuming a 'success' field in the response
            log_test_result(description, True)
            print(f"   Updated Note ID: {note_id}")
        else:
            log_test_result(description, False, "Update operation failed.")
    except Exception as e:
        log_test_result(description, False, e)


if __name__ == "__main__":
    test_update_note()
