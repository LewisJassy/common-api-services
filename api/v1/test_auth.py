import unittest
from auth import authenticate, TokenExpiredError

class TestAuth(unittest.TestCase):
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