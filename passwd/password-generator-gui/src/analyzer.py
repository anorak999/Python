def analyze_password(password):
    import string

    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    score = sum([has_upper, has_lower, has_digit, has_symbol]) + (length >= 12)
    verdicts = [
        "Very Weak: Easily guessable. Avoid using common words or short passwords.",
        "Weak: Add more character types and increase length.",
        "Moderate: Consider adding symbols and more length.",
        "Strong: Good, but longer is better.",
        "Very Strong: Excellent, but avoid using personal info.",
        "Excellent: Your password is very strong!"
    ]
    verdict = verdicts[min(score, len(verdicts)-1)]

    suggestions = []
    if length < 12:
        suggestions.append("- Make your password at least 12 characters long.")
    if not has_upper:
        suggestions.append("- Add uppercase letters.")
    if not has_lower:
        suggestions.append("- Add lowercase letters.")
    if not has_digit:
        suggestions.append("- Add digits.")
    if not has_symbol:
        suggestions.append("- Add special symbols.")

    analysis = f"Password: {password}\n"
    analysis += f"Length: {length}\n"
    analysis += f"Contains uppercase: {'Yes' if has_upper else 'No'}\n"
    analysis += f"Contains lowercase: {'Yes' if has_lower else 'No'}\n"
    analysis += f"Contains digit: {'Yes' if has_digit else 'No'}\n"
    analysis += f"Contains symbol: {'Yes' if has_symbol else 'No'}\n"
    analysis += f"\nStrength Verdict: {verdict}\n"
    if suggestions:
        analysis += "\nSuggestions to improve:\n" + "\n".join(suggestions)
    else:
        analysis += "\nGreat job! Your password is strong."

    return analysis

def has_common_patterns(password):
    common_patterns = ["123456", "password", "qwerty", "abc123", "letmein"]
    return any(pattern in password for pattern in common_patterns)

def analyze(password):
    strength, criteria = analyze_password(password)
    common = has_common_patterns(password)
    return {
        "strength": strength,
        "criteria": criteria,
        "common_patterns": common,
    }