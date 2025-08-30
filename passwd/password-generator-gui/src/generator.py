import random
import string

class PasswordGenerator:
    def generate_password(self, length):
        if length < 1:
            raise ValueError("Password length must be at least 1")
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def get_brute_force_time(self, password):
        charset_size = len(string.ascii_letters + string.digits + string.punctuation)
        attempts = charset_size ** len(password)
        time_per_attempt = 0.0000001  # 0.1 microseconds per attempt
        total_time_seconds = attempts * time_per_attempt
        if total_time_seconds < 60:
            return f"{total_time_seconds:.2f} seconds"
        elif total_time_seconds < 3600:
            return f"{total_time_seconds / 60:.2f} minutes"
        else:
            return f"{total_time_seconds / 3600:.2f} hours"