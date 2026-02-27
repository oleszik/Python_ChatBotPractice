# Python ChatBot Practice

A simple terminal chatbot built in Python. It greets the user, guesses age from remainders, counts to a target number, runs a multiple-choice quiz, and provides a small command menu for repeated sessions.

## Features

- Input validation with retry prompts for invalid numbers
- Dynamic bot configuration through CLI args and environment variables
- Age guessing using modulo arithmetic (3, 5, and 7)
- Counting flow with non-negative integer validation
- Quiz with:
  - Multiple questions
  - Randomized question order
  - Per-question correctness feedback
  - Final score and summary feedback
- Command menu after each session:
  - `help`
  - `restart`
  - `exit`
- Graceful exit handling for `Ctrl+C` and `Ctrl+D`/EOF
- Unit tests for age logic and quiz behavior (`pytest`)

## Requirements

- Python 3.10+

## Run The Chatbot

Default run:

```powershell
python ChatBot.py
```

Use CLI args:

```powershell
python ChatBot.py --name Nova --birth-year 2026
```

Use environment variables (PowerShell):

```powershell
$env:CHATBOT_NAME = "Nova"
$env:CHATBOT_BIRTH_YEAR = "2026"
python ChatBot.py
```

## Menu Commands

After the first chatbot run, use:

- `help` to print command help
- `restart` to run the full chatbot flow again
- `exit` to quit

## Run Tests

Install test dependency:

```powershell
python -m pip install -r requirements-dev.txt
```

Run tests:

```powershell
python -m pytest -q
```

## Project Structure

- `ChatBot.py` - main chatbot app
- `tests/test_chatbot.py` - unit tests
- `requirements-dev.txt` - dev/test dependencies
