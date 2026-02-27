import argparse
import os
import random
from dataclasses import dataclass


DEFAULT_BOT_NAME = "Aid"
DEFAULT_BIRTH_YEAR = 2023
ENV_BOT_NAME = "CHATBOT_NAME"
ENV_BIRTH_YEAR = "CHATBOT_BIRTH_YEAR"


@dataclass(frozen=True)
class QuizQuestion:
    prompt: str
    options: tuple[str, ...]
    correct_option: int


QUIZ_QUESTIONS = (
    QuizQuestion(
        prompt="Why do we use methods?",
        options=(
            "To repeat a statement multiple times.",
            "To decompose a program into several small subroutines.",
            "To determine the execution time of a program.",
            "To interrupt the execution of a program.",
        ),
        correct_option=2,
    ),
    QuizQuestion(
        prompt="Which data type stores True/False values?",
        options=("str", "int", "bool", "float"),
        correct_option=3,
    ),
    QuizQuestion(
        prompt="What does `len('chat')` return?",
        options=("3", "4", "5", "An error"),
        correct_option=2,
    ),
    QuizQuestion(
        prompt="Which keyword defines a function in Python?",
        options=("func", "define", "def", "lambda"),
        correct_option=3,
    ),
)


def parse_env_int(var_name, default):
    raw_value = os.getenv(var_name)
    if raw_value is None:
        return default
    try:
        return int(raw_value)
    except ValueError:
        return default


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Simple Python chatbot.")
    parser.add_argument(
        "--name",
        default=os.getenv(ENV_BOT_NAME, DEFAULT_BOT_NAME),
        help=f"Bot name (or set {ENV_BOT_NAME}).",
    )
    parser.add_argument(
        "--birth-year",
        type=int,
        default=parse_env_int(ENV_BIRTH_YEAR, DEFAULT_BIRTH_YEAR),
        help=f"Bot birth year (or set {ENV_BIRTH_YEAR}).",
    )
    return parser.parse_args(argv)


def read_text(prompt, input_fn=input, output_fn=print):
    while True:
        value = input_fn(f"{prompt} ").strip()
        if value:
            return value
        output_fn("Please enter some text.")


def read_int(prompt, min_value=None, max_value=None, input_fn=input, output_fn=print):
    while True:
        raw_value = input_fn(f"{prompt} ").strip()
        try:
            value = int(raw_value)
        except ValueError:
            output_fn("Please enter a whole number.")
            continue

        if min_value is not None and max_value is not None:
            if not min_value <= value <= max_value:
                output_fn(f"Please enter a number from {min_value} to {max_value}.")
                continue
        elif min_value is not None and value < min_value:
            output_fn(f"Please enter a number greater than or equal to {min_value}.")
            continue
        elif max_value is not None and value > max_value:
            output_fn(f"Please enter a number less than or equal to {max_value}.")
            continue
        return value


def greet(bot_name, birth_year, output_fn=print):
    output_fn(f"Hello! My name is {bot_name}.")
    output_fn(f"I was created in {birth_year}.")


def remind_name(input_fn=input, output_fn=print):
    name = read_text("Please remind me of your name:", input_fn=input_fn, output_fn=output_fn)
    output_fn(f"What a great name you have, {name}!")


def calculate_age(rem3, rem5, rem7):
    return (rem3 * 70 + rem5 * 21 + rem7 * 15) % 105


def guess_age(input_fn=input, output_fn=print):
    output_fn("Let me guess your age.")
    output_fn("Enter remainders of dividing your age by 3, 5, and 7.")
    rem3 = read_int("Remainder when divided by 3:", 0, 2, input_fn=input_fn, output_fn=output_fn)
    rem5 = read_int("Remainder when divided by 5:", 0, 4, input_fn=input_fn, output_fn=output_fn)
    rem7 = read_int("Remainder when divided by 7:", 0, 6, input_fn=input_fn, output_fn=output_fn)
    age = calculate_age(rem3, rem5, rem7)
    output_fn(f"Your age is {age}; that's a good time to start programming!")


def build_count_sequence(num):
    return range(num + 1)


def count(input_fn=input, output_fn=print):
    output_fn("Now I will prove to you that I can count to any number you want.")
    num = read_int("Enter a non-negative number:", 0, input_fn=input_fn, output_fn=output_fn)
    for number in build_count_sequence(num):
        output_fn(f"{number}!")


def get_shuffled_quiz_questions(rng=None):
    questions = list(QUIZ_QUESTIONS)
    if rng is None:
        rng = random.Random()
    rng.shuffle(questions)
    return questions


def score_quiz_answers(questions, answers):
    return sum(1 for question, answer in zip(questions, answers) if answer == question.correct_option)


def quiz_feedback(score, total):
    if score == total:
        return "Excellent work. You got everything right."
    if score >= (total * 0.6):
        return "Nice job. You have a good grasp of the basics."
    return "Good effort. Keep practicing and try again."


def run_quiz(questions, input_fn=input, output_fn=print):
    output_fn("Let's test your programming knowledge.")
    answers = []
    for index, question in enumerate(questions, start=1):
        output_fn(f"Question {index}: {question.prompt}")
        for option_index, option in enumerate(question.options, start=1):
            output_fn(f"{option_index}. {option}")
        answer = read_int(
            "Your answer (enter option number):",
            1,
            len(question.options),
            input_fn=input_fn,
            output_fn=output_fn,
        )
        answers.append(answer)
        if answer == question.correct_option:
            output_fn("Correct.")
        else:
            output_fn(f"Not quite. The correct answer is {question.correct_option}.")

    score = score_quiz_answers(questions, answers)
    total = len(questions)
    output_fn(f"You scored {score}/{total}.")
    output_fn(quiz_feedback(score, total))
    return score


def end(output_fn=print):
    output_fn("Congratulations, have a nice day!")


def show_help(output_fn=print):
    output_fn("Menu commands:")
    output_fn("help    - Show available commands.")
    output_fn("restart - Run the chatbot flow again.")
    output_fn("exit    - Quit the chatbot.")


def run_chatbot_session(bot_name, birth_year, input_fn=input, output_fn=print):
    greet(bot_name, birth_year, output_fn=output_fn)
    remind_name(input_fn=input_fn, output_fn=output_fn)
    guess_age(input_fn=input_fn, output_fn=output_fn)
    count(input_fn=input_fn, output_fn=output_fn)
    run_quiz(get_shuffled_quiz_questions(), input_fn=input_fn, output_fn=output_fn)
    end(output_fn=output_fn)


def command_menu_loop(bot_name, birth_year, input_fn=input, output_fn=print):
    show_help(output_fn=output_fn)
    while True:
        command = input_fn("Menu command (help/restart/exit): ").strip().lower()
        if command == "help":
            show_help(output_fn=output_fn)
        elif command == "restart":
            run_chatbot_session(bot_name, birth_year, input_fn=input_fn, output_fn=output_fn)
        elif command == "exit":
            output_fn("Session ended. Goodbye!")
            return
        else:
            output_fn("Unknown command. Type 'help' to view options.")


def main(argv=None):
    args = parse_args(argv)
    run_chatbot_session(args.name, args.birth_year)
    command_menu_loop(args.name, args.birth_year)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nSession ended. Goodbye!")
