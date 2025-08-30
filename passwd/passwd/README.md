# Password Generator Project

This project is a Python-based password generator that creates secure passwords and estimates the time it would take to brute-force them using popular tools like Maduze or John the Ripper.

## Features

- **Password Generation**: Generate random passwords of specified lengths.
- **Strength Estimation**: Evaluate the strength of generated passwords based on length and character variety.
- **Brute-force Time Estimation**: Calculate the estimated time required to brute-force a password.

## Project Structure

```
passwd
├── src
│   ├── __init__.py
│   ├── generator.py
│   ├── strength_estimator.py
│   └── utils.py
├── tests
│   ├── __init__.py
│   ├── test_generator.py
│   └── test_strength_estimator.py
├── requirements.txt
└── README.md
```

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

1. Import the `PasswordGenerator` class from `src.generator`.
2. Use the `generate_password(length)` method to create a password.
3. Use the `get_brute_force_time(password)` method to estimate the brute-force time.

Example:

```python
from src.generator import PasswordGenerator

generator = PasswordGenerator()
password = generator.generate_password(12)
time_to_bruteforce = generator.get_brute_force_time(password)
print(f"Generated Password: {password}")
print(f"Estimated Brute-force Time: {time_to_bruteforce}")
```

## Testing

To run the tests, navigate to the `tests` directory and execute:

```
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.