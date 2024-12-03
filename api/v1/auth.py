import bcrypt
import jwt
from datetime import datetime, timedelta
import os
import sqlite3

# Secret key for JWT token generation
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

# Initialize SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password TEXT
)
''')
conn.commit()

def register_user(email: str, password: str) -> dict:
    """
    Registers a new user with email and password.
    Args:
        email(str): User's email address.
        password(str): User's password.
    
    Returns:
        dict: User details along with a success message.
    """
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    if cursor.fetchone():
        raise ValueError("Email already registered.")
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
        conn.commit()

    return {'message': 'User registered successfully.', 'email': email}

def authenticate_user(email: str, password: str) -> str:
    """
    Authenticate a user by verifying the email and password.

    Args:
        email(str): User's email address.
        password(str): User's password.
    
    Returns:
        str: JWT token if the user is authenticated, otherwise None.
    """
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user[1]):
        raise ValueError('Invalid email or password')
    
    token = jwt.encode(
        {'email': email, 'exp': datetime.utcnow() + timedelta(minutes=30)},
        SECRET_KEY,
        algorithm='HS256'
    )

    return token

def validate_token(token: str) -> dict:
    """
    Validate a JWT token and decodes its payload.

    Args:
        token(str): JWT token to be validated.
    
    Returns:
        dict: User details if the token is valid, otherwise None.
    
    Raises:
        jwt.ExpiredSignatureError: If the token is expired.
        jwt.InvalidTokenError: If the token is invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('Token expired')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token')

def oauth_login(provider: str, token: str) -> dict:
    """
    Handles OAuth-based login

    Args:
        provider(str): OAuth provider name.(eg. google.com, facebook.com)
        token(str): OAuth token.
    
    Returns:
        dict: User details if the login is successful, otherwise None.
    
    Note:
        Replace this function's implementation with the provider-specific API calls
    """
    if provider.lower() == "google" and token == "google_token":
        return {"message": "Google login successful", "email": "user@google.com"}
    elif provider.lower() == "facebook" and token == "facebook_token":
        return {"message": "Facebook login successful", "email": "user@facebook.com"}
    else:
        return {"message": "Invalid OAuth provider or token"}
