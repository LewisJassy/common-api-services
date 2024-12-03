"""
auth.py

Provides authentiaction-related functionality, including user login, registration, and OAuth integration.
"""
import bcrypt
import jwt
from datetime import datetime, timedelta
import os

# Secret key for JWT token generation
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

# In-memory user store for demo purposes(replace with database in production)
USER_STORE = {}

def register_user(email:str, password:str) -> dict:
    """
    Registers a new user with first name, last name, email, and password.
    Args:
        first_name(str): User's first name.
        last_name(str): User's last name.
        email(str): User's email address.
        password(str): User's password.
    
    Returns:
        dict: User details along with a success message.
    """

    if email in USER_STORE:
        raise ValueError("Email already registered.")
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        USER_STORE[email] = {'email': email, 'password': hashed_password}

    return {'message': 'User registered successfully.', 'email': email}


def authenticate_user(email: str, password: str) ->str:
    """
    Authenticate a user by verifying the email and password.

    Args:
        email(str): User's email address.
        password(str): User's password.
    
    Returns:
        str: JWT token if the user is authenticated, otherwise None.
    """

    user = USER_STORE.get(email)
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        raise ValueError('Invalid email or password')
    
    token = jwt.encode(
        {'email': email, 'exp': datetime.now(UTC) + timedelta(minutes=30)},
        SECRET_KEY,
        algorithm='HS256'
    )

    return token

def validate_token(token:str) -> dict:
    """"
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


def oauth_login(provider:str, token:str) -> dict:
    """
    Handles OAuth-based login

    Args:
        provider(str): OAuth provider name.(eg. google.com, facebook.com)
        token(str): OAuth token.
    
    Returns:
        dict: User details if the login is successful, otherwise None.
    
    Note:
        Replace tis function's implementation with the provider-specific API calls
    """

    if provider.lower() == "google" and token == "google_token":
        return {"message": "Google login successful", "email": "user@gooogle.com"}
    elif provider.lower() == "facebook" and token == "facebook_token":
        return {"message": "Facebook login successful", "email": "user@facebook.com"}
    else:
        return {"message": "Invalid OAuth provider or token"}
    

