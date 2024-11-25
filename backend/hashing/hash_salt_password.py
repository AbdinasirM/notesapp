import bcrypt

def generate_salt() -> bytes:
    """Generate a new salt."""
    return bcrypt.gensalt()

def hash_password(password: str, salt: bytes) -> str:
    """
    Hash a password with the provided salt.
    
    Args:
        password (str): The password to hash.
        salt (bytes): The salt to use for hashing.
    
    Returns:
        str: The salted, hashed password.
    """
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()  # Return as a string for storage

'''
for sign up
hash and salt the provided password
save that user email, hashed and salted password to the db = {}
generate a token and return it to be saved on the client

for sign in 
take the user email and password from the user
fetch the user email(unique), hashed and salted password and the salt
verify the credentials by:
take the plain text password  and encode it with the salt that was saved
compare the stored hash and salted password with the new hashed and salted password
if true :
generate a jwt token to save in the client:
it takes user email, 
expirate time,
generated at
and then return the token to the client and show a welcome message

'''


