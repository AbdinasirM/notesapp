def log_test_result(description, passed, error=None):
    """Simulates Jest-like test result output with emojis."""
    if passed:
        print(f"✅ {description}")
    else:
        print(f"❌ {description}")
        if error:
            print(f"   🛑 Error: {error}")

