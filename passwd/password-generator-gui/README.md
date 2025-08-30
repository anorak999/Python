# Password Generator GUI

This project is a password generator application with a graphical user interface (GUI) that allows users to create secure passwords and analyze their strength. It is designed to help users generate strong passwords and understand the factors that contribute to password security.

## Features

- Generate random passwords of specified lengths.
- Analyze the strength of generated passwords based on various criteria.
- User-friendly GUI for easy interaction.

## Project Structure

```
password-generator-gui
├── src
│   ├── generator.py      # Contains the PasswordGenerator class for password generation.
│   ├── gui.py            # Implements the GUI for the password generator.
│   ├── analyzer.py       # Contains functions for analyzing password strength.
│   └── utils.py          # Utility functions for input validation and constants.
├── requirements.txt       # Lists the dependencies required for the project.
└── README.md              # Documentation for the project.
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd password-generator-gui
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python src/gui.py
   ```

2. Use the GUI to generate passwords and analyze their strength.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.