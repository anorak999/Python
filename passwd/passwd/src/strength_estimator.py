class StrengthEstimator:
    def estimate_strength(self, password):
        length = len(password)
        variety = len(set(password))
        
        if length < 8:
            return "Weak"
        elif length < 12:
            return "Moderate"
        elif variety < 4:
            return "Moderate"
        else:
            return "Strong"

    def get_time_to_bruteforce(self, password):
        length = len(password)
        charset_size = 95  # Assuming ASCII printable characters
        combinations = charset_size ** length
        time_seconds = combinations / 1000000000  # Assuming 1 billion guesses per second
        return time_seconds