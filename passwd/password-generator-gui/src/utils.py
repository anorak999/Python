def validate_password_length(length):
    if length < 1:
        raise ValueError("Password length must be at least 1")

def is_strong_password(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char in string.punctuation for char in password):
        return False
    return True

def get_common_patterns():
    return ["123456", "password", "12345678", "qwerty", "abc123", "letmein", "monkey", "111111", "1234567", "sunshine"]