import bcrypt

def verify_password(provided_password: str, stored_hashed_password: str, salt: bytes) -> bool:
    """
    Verify a password against the stored hash and salt.
    
    Args:
        provided_password (str): The password provided by the user.
        stored_hashed_password (str): The previously stored hashed password.
        salt (bytes): The salt used during hashing.
    
    Returns:
        bool: True if the password matches, False otherwise.
    """
    new_hashed_password = bcrypt.hashpw(provided_password.encode(), salt)
    return new_hashed_password.decode() == stored_hashed_password
