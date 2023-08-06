import re
import subprocess
import sys
import random
import unicodedata
from qb_gen.constants import UPPERCASE_LETTERS, LOWERCASE_LETTERS, NUMERIC_LETTERS


def concat_strings(list_of_strings: list[str]) -> list[str]:
    """Return a list of strings which concat from the given list of strings

    Args:
        list_of_strings (list[str]): the original list of string to concat

    Returns:
        list[str]: a list of concatenated string
    """

    # Base case: if the input list has only one string, return a list with that string
    if len(list_of_strings) == 1:
        return list_of_strings

    # Recursive case: concatenate the first string with all possible combinations
    # of the remaining strings
    result = []
    for i in range(len(list_of_strings)):
        first_string = list_of_strings[i]
        remaining_strings = list_of_strings[:i] + list_of_strings[i + 1 :]
        for s in concat_strings(remaining_strings):
            result.append(first_string + s)

            # Return early to prevent bottle neck
            if len(result) >= 4:
                break

    return result


def remove_accents(s):
    """Remove language accent from a string

    Args:
        s (str)

    Returns:
        str: String with no language accent
    """
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode("utf-8")


def move_first_letter_to_front(s: str) -> str:
    """Move the first alphabetic character to the front of a given string

    Args:
        s (str)

    Returns:
        str: Modified string with the first letter is an alphabetic character.
    """
    if s[0].isalpha():
        return s

    # Find the first letter in the string
    for i, char in enumerate(s):
        if char.isalpha():
            # Return the string with the letter moved to the front
            return char + s[:i] + s[i + 1 :]
    # If there are no letters in the string, return the original string
    return s


def copy_to_clipboard(text: str) -> None:
    """Copy a string clipboard

    Args:
        text (str): Text to copy
    """
    if sys.platform == "win32":
        # For Windows
        subprocess.run(["clip.exe"], input=text.strip(), check=True)
    elif sys.platform == "darwin":
        # For macOS
        subprocess.run(["pbcopy"], universal_newlines=True, input=text, check=True)
    else:
        # For Linux
        subprocess.run(["xsel", "-bi"], input=text, check=True)


def longest_common_substring(
    string1: str, string2: str, case_sensitive: bool = False
) -> str:
    """Find the common substring from 2 strings.

    Args:
        string1 (str): First string.
        string2 (str): Second string.
        case_sensitive (bool, optional): If True, the case of the letters will matter. Defaults to False.

    Returns:
        str: Common substring.
    """
    # Make strings lowercase if case sensitivity is not required
    if not case_sensitive:
        string1 = string1.lower()
        string2 = string2.lower()

    # Initialize the matrix for storing substring lengths
    substring_lengths = [[0] * (1 + len(string2)) for i in range(1 + len(string1))]

    # Initialize longest substring length and its ending position
    longest_length, longest_end = 0, 0

    # Iterate through each character in the strings
    for i, char1 in enumerate(string1):
        for j, char2 in enumerate(string2):
            # If characters are the same, increase the substring length
            if char1 == char2:
                substring_lengths[i + 1][j + 1] = substring_lengths[i][j] + 1

                # Update longest substring length and position if necessary
                if substring_lengths[i + 1][j + 1] > longest_length:
                    longest_length = substring_lengths[i + 1][j + 1]
                    longest_end = i + 1
            else:
                # Reset substring length to 0 if characters are different
                substring_lengths[i + 1][j + 1] = 0

    # Return the longest common substring
    return string1[longest_end - longest_length : longest_end]


def detect_repeated_substring(s: str) -> str:
    """Check for a substring that is repeated at least 3 times in a row in a string

    Args:
        s (str): string to check

    Returns:
        str: The repeated substring if found, otherwise None
    """
    pattern = r"(.+)\1{2,}"
    match = re.search(pattern, s)

    if match:
        return match.group(1)
    return None


def alternate_case_in_string(s: str) -> str:
    """Randomly alternate the case of the letters in a given string

    Args:
        s (str):

    Returns:
        str
    """

    result = "".join(
        [char.upper() if random.random() > 0.5 else char.lower() for char in s]
    )

    return result


def generate_new_str(s: str) -> str:
    """Generate a new string based on the old one

    Args:
        word (str): old string

    Returns:
        str: new string
    """
    if len(s) == 0:
        return s

    uppercase_replacement = [c for c in UPPERCASE_LETTERS if c not in s]
    lowercase_replacement = [c for c in LOWERCASE_LETTERS if c not in s]
    number_replacement = [c for c in NUMERIC_LETTERS if c not in s]

    new_str = ""
    for char in s:
        if char.isupper():
            new_str += random.choice(uppercase_replacement)

        elif char.islower():
            new_str += random.choice(lowercase_replacement)

        elif char.isnumeric():
            new_str += random.choice(number_replacement)

        else:
            new_str += char

    return new_str
