import hashlib
from models import User
from sqlalchemy import func

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    user = User.query.filter(func.lower(User.username) == username.lower()).first()
    if user:
        print(f"User found: {user.username}, stored hash: {user.password}")
        print(f"Input password length: {len(password)}")
        print(f"Input hash: {hash_password(password)}")
        if user.password == hash_password(password):
            print("Login successful")
            return user
        print("Password mismatch")
    else:
        print(f"No user found for username: {username}")
    return None