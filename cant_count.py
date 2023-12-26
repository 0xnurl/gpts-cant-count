import itertools
import operator
import os
import re
import sys
import argparse

from loguru import logger
import openai

logger.remove()
logger.add(sys.stderr, level="INFO")

_MODEL = "gpt-3.5-turbo"
_API_KEY = os.getenv("OPENAI_API_KEY")

_CLIENT = openai.OpenAI(api_key=_API_KEY)


def _send_request(prompt):
    return _CLIENT.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=_MODEL,
    )


def _str_to_int(s):
    return int(s.replace(",", ""))


def _extract_ints_from_string(s) -> list[int]:
    return list(map(_str_to_int, re.findall(r"[\d,]+", s)))


def _get_response_answers(response) -> tuple[int, ...]:
    ints = []
    for choice in response.choices:
        ints += _extract_ints_from_string(choice.message.content)

    return tuple(ints)


def _send_and_verify(a, b, op, operator_func):
    prompt = f"{a}{op}{b}="
    response = _send_request(prompt)
    answers = _get_response_answers(response)
    target = operator_func(a, b)
    return any(answer == target for answer in answers), response


def run(min_n, max_n, max_attempts, op):
    # Up-only binary search of the range.
    operator_func = {
        "+": operator.add,
        "*": operator.mul,
        "-": operator.sub,
    }[op]

    all_combinations = tuple(itertools.product(range(min_n, max_n + 1), repeat=2))
    curr_idx = 0
    max_idx = len(all_combinations) - 1
    next_idx = max_idx // 2

    logger.info(f"Running from {min_n:,} to {max_n:,}, operator '{op}'...")

    num_attempts = 0
    while num_attempts < max_attempts:
        num_attempts += 1

        a, b = all_combinations[curr_idx]
        logger.debug(f"Testing {a:,} {op} {b:,}")
        is_correct, response = _send_and_verify(a, b, op, operator_func)

        if is_correct:
            logger.info(f"{a:,} {op} {b:,} correct.")
            logger.debug(
                f"Model answered correctly: '{response.choices[0].message.content}'."
            )
            curr_idx = next_idx
            next_idx = ((max_idx - next_idx) // 2) + next_idx
            logger.debug(f"Next idx: {next_idx}")
        else:
            logger.info(f"{a:,} {op} {b:,} INCORRECT!!!")
            logger.info(f"Model answered: '{response.choices[0].message.content}'.")
            logger.info(f"Correct answer was: {operator_func(a,b):,}.")
            break

    logger.info(f"Done after {num_attempts} attempts.")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--min",
        type=int,
        required=True,
    )
    arg_parser.add_argument(
        "--max",
        type=int,
        required=True,
    )
    arg_parser.add_argument(
        "--max_attempts",
        type=int,
        required=True,
    )
    arg_parser.add_argument(
        "--op",
        type=str,
        default="+",
    )
    options = arg_parser.parse_args()

    run(
        min_n=options.min,
        max_n=options.max,
        max_attempts=options.max_attempts,
        op=options.op,
    )
