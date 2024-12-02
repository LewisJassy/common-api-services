import unittest
from auth import authenticate_user, validate_token, register_user

class TestAuth(unittest.TestCase):

    def setUp(self):
        # Set up a test user
        self.email = "test@example.com"
        self.password = "password123"
        register_user("Test", "User", self.email, self.password)

    def test_valid_credentials(self):
        self.assertTrue(authenticate('valid_user', 'valid_password'))

    def test_invalid_credentials(self):
        self.assertFalse(authenticate('invalid_user', 'invalid_password'))

    def test_token_expiration(self):
        with self.assertRaises(TokenExpiredError):
            authenticate('user_with_expired_token', 'password')

    def test_empty_credentials(self):
        self.assertFalse(authenticate('', ''))

    def test_special_characters_in_credentials(self):
        self.assertTrue(authenticate('user!@#$', 'pass!@#$'))

if __name__ == '__main__':
    unittest.main()