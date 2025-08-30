import unittest
from src.strength_estimator import StrengthEstimator

class TestStrengthEstimator(unittest.TestCase):

    def setUp(self):
        self.estimator = StrengthEstimator()

    def test_estimate_strength(self):
        self.assertEqual(self.estimator.estimate_strength("123456"), "Weak")
        self.assertEqual(self.estimator.estimate_strength("Password123!"), "Strong")
        self.assertEqual(self.estimator.estimate_strength("abc"), "Very Weak")
        self.assertEqual(self.estimator.estimate_strength("A1!b2@C3#"), "Very Strong")

    def test_get_time_to_bruteforce(self):
        self.assertGreater(self.estimator.get_time_to_bruteforce("123456"), 0)
        self.assertGreater(self.estimator.get_time_to_bruteforce("Password123!"), 0)
        self.assertGreater(self.estimator.get_time_to_bruteforce("abc"), 0)
        self.assertGreater(self.estimator.get_time_to_bruteforce("A1!b2@C3#"), 0)

if __name__ == '__main__':
    unittest.main()