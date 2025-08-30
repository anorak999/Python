import unittest
from src.generator import PasswordGenerator

class TestPasswordGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = PasswordGenerator()

    def test_generate_password_length(self):
        password = self.generator.generate_password(12)
        self.assertEqual(len(password), 12)

    def test_generate_password_characters(self):
        password = self.generator.generate_password(12)
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in '!@#$%^&*()_+' for c in password))

    def test_get_brute_force_time(self):
        password = self.generator.generate_password(12)
        time_estimate = self.generator.get_brute_force_time(password)
        self.assertIsInstance(time_estimate, float)

if __name__ == '__main__':
    unittest.main()