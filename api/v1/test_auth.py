import unittest
from auth import authenticate_user, validate_token, register_user, conn, cursor
import bcrypt
import jwt
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

class TestAuth(unittest.TestCase):

    def setUp(self):
        # Clear the database before each test
        cursor.execute('DELETE FROM users')
        conn.commit()
        # Set up a test user
        self.email = fake.email()
        self.password = fake.password()
        register_user(self.email, self.password)

    def test_valid_credentials(self):
        token = authenticate_user(self.email, self.password)
        self.assertIsNotNone(token)

    def test_invalid_credentials(self):
        with self.assertRaises(ValueError):
            authenticate_user("invalid@example.com", "wrongpassword")

    def test_token_expiration(self):
        token = jwt.encode(
            {'email': self.email, 'exp': datetime.utcnow() - timedelta(seconds=1)},
            'default_secret_key',
            algorithm='HS256'
        )
        with self.assertRaises(ValueError):
            validate_token(token)

    def test_empty_credentials(self):
        with self.assertRaises(ValueError):
            authenticate_user("", "")

    def test_special_characters_in_credentials(self):
        email = "special@example.com"
        password = "pass!@#$"
        register_user(email, password)
        token = authenticate_user(email, password)
        self.assertIsNotNone(token)

if __name__ == '__main__':
    unittest.main()