import random
from unidecode import unidecode
from itertools import chain
from typing import Union

from qb_gen.utils import (
    longest_common_substring,
    detect_repeated_substring,
    move_first_letter_to_front,
    alternate_case_in_string,
    concat_strings,
    generate_new_str,
)
from qb_gen.constants import (
    UPPERCASE_LETTERS,
    LOWERCASE_LETTERS,
    NUMERIC_LETTERS,
    SPECIAL_CHARACTERS,
    UNSUITABLE_SPECIAL_CHARACTER,
    SUITABLE_SPECIAL_CHARACTERS,
    SPECIAL_CHARACTERS_FOR_LETTER_REPLACEMENT,
    NUMERIC_CHARACTERS_FOR_LETTER_REPLACEMENT,
    PASSWORD_GOOD_FEATURES,
    PASSWORD_BAD_FEATURES,
)


# ********* Password Generator ********* #


def generate_password(
    length: int = 12, contain_special_character: bool = True, avoid_common: bool = False
) -> str:
    """Generate a secure password

    Args:
        length (int, optional): Length of the password, must be at least 9. Defaults to 12.
        contain_special_character (bool, optional): If True, special characters will be included to the passwords. Defaults to True.
        avoid_common (bool, optional): If True, the program will validate and try to avoid any substring that similar to the most used passwords/words. Defaults to False.

    Raises:
        Exception: Invalid password length.

    Returns:
        str: Generated password.
    """
    if length <= 0:
        raise Exception("Invalid password length.")
    elif length <= 8:
        return generate_password_with_short_length(length)

    generated_pwd = ""

    remaining_length = length

    # Add special characters
    if contain_special_character:
        special_part = random.choices(
            SUITABLE_SPECIAL_CHARACTERS, k=random.randint(1, length // 5)
        )
        special_part = "".join(special_part)
        generated_pwd += special_part
        remaining_length -= len(special_part)

    while True:
        if remaining_length == 0:
            break

        # Add numeric characters
        numeric_part = random.choices(NUMERIC_LETTERS, k=random.randint(1, length // 4))
        numeric_part = "".join(numeric_part)
        generated_pwd += numeric_part
        remaining_length -= len(numeric_part)

        # Add uppercase letters
        uppercase_part = random.choices(
            UPPERCASE_LETTERS, k=random.randint(1, remaining_length // 2)
        )
        uppercase_part = "".join(uppercase_part)
        generated_pwd += uppercase_part
        remaining_length -= len(uppercase_part)

        # Add lowercase letters
        lowercase_part = random.choices(LOWERCASE_LETTERS, k=remaining_length)
        lowercase_part = "".join(lowercase_part)
        generated_pwd += lowercase_part
        remaining_length -= len(lowercase_part)

    # Shuffle the generated string
    generated_pwd = "".join(random.sample(generated_pwd, len(generated_pwd)))

    # First character of a password should be a letter
    generated_pwd = move_first_letter_to_front(generated_pwd)

    # Avoid common password or common word
    if avoid_common:
        generated_pwd = avoid_common_word_and_pwd(generated_pwd)

    return generated_pwd


def generate_password_with_short_length(length: int) -> str:
    """Generate password with inefficient length (equal or lower than 8)

    Args:
        length (int): password's length

    Returns:
        str: generated password
    """
    if length <= 0:
        raise Exception("Invalid password length.")

    if 1 <= length <= 3:
        password = "".join(random.sample(LOWERCASE_LETTERS, length))
        return password if length == 1 else alternate_case_in_string(password)

    # Choose randomly a number and a special character
    numeric_n_special_characters = random.choice(
        SUITABLE_SPECIAL_CHARACTERS
    ) + random.choice(NUMERIC_LETTERS)

    # Choose randomly lower and uppercase letters
    lowercase_letters = random.choices(LOWERCASE_LETTERS, k=(length - 2) // 2)
    uppercase_letters = random.choices(
        UPPERCASE_LETTERS, k=((length - 2) - ((length - 2) // 2))
    )

    generated_pwd = numeric_n_special_characters + "".join(
        lowercase_letters + uppercase_letters
    )

    # Shuffle the generated string
    generated_pwd = "".join(random.sample(generated_pwd, len(generated_pwd)))

    # First character of a password should be a letter
    generated_pwd = move_first_letter_to_front(generated_pwd)
    return generated_pwd


def generate_password_from_user_input(
    user_input: str,
    max_strength: bool = False,
    additional_words: list[str] = None,
    all_variants: bool = False,
) -> Union[list[str], str]:
    """Generate a password from an user's input (a favorite quote, a favorite words, ...)

    Args:
        user_input (str): user's input
        max_strength (bool, optional): if True, only return the generated password with the highest password strength. Defaults to False.
        additional_words (list[str], optional): add additional words to the password for it easier to remember.
        all_variants (bool, optional): return all generated passwords (include all combinations of additional words with the passwords)

    Returns:
        Union[list[str], str]: A single or a list of generated passwords.
    """
    if additional_words is None:
        additional_words = []

    # Remove white spaces from each word in the list additional words
    if len(additional_words) > 0:
        additional_words = [word.replace(" ", "") for word in additional_words]

    # Remove user's input accent
    user_input = unidecode(user_input)

    # Remove unsuitable special characters from user' input
    user_input = "".join(
        filter(lambda char: char not in UNSUITABLE_SPECIAL_CHARACTER, user_input)
    )

    # Generate a passwords with the highest password strength
    highest_strength_password = generate_password_from_full_content(
        user_input,
        contain_special_character=True,
        alternate_case=True,
        enhance_password_strength=True,
    )

    if max_strength:
        if len(additional_words) > 0:
            additional_texts = "".join(additional_words)
            highest_strength_password += additional_texts

        return highest_strength_password

    # Generate a list of passwords
    list_of_generated_passwords = [
        highest_strength_password,
    ]

    # Limited the variants of generated passwords
    if not all_variants:
        # simplified
        list_of_generated_passwords.append(
            generate_password_from_content_simplified(user_input)
        )
        list_of_generated_passwords.append(
            generate_password_from_content_simplified(user_input, alternate_case=True)
        )
        list_of_generated_passwords.append(
            generate_password_from_content_simplified(
                user_input, contain_special_character=True, alternate_case=True
            )
        )

        # full content
        list_of_generated_passwords.append(
            generate_password_from_full_content(user_input)
        )
        list_of_generated_passwords.append(
            generate_password_from_full_content(
                user_input, contain_special_character=True
            )
        )
        list_of_generated_passwords.append(
            generate_password_from_full_content(
                user_input, contain_special_character=True, alternate_case=True
            )
        )

        # Remove duplicate passwords and sort them by length
        list_of_generated_passwords = sorted(
            list(filter(lambda p: p != "", set(list_of_generated_passwords))),
            key=lambda el: len(el),
        )

        # Add additional words
        if len(additional_words) > 0:
            additional_texts = "".join(additional_words)
            list_of_generated_passwords = [
                pwd + additional_texts for pwd in list_of_generated_passwords
            ]

    # Return all the variants of the generated passwords
    else:
        # Create a list of generated passwords using different generate_methods
        for generate_method in (
            generate_password_from_content_simplified,
            generate_password_from_full_content,
        ):
            # Try generating passwords with and without special characters
            for contain_special_character in (True, False):
                # Try generating passwords with and without alternating case
                for alternate_case in (True, False):
                    list_of_generated_passwords.append(
                        generate_method(
                            user_input, contain_special_character, alternate_case
                        )
                    )

        # Remove duplicate passwords and sort them by length
        list_of_generated_passwords = sorted(
            list(filter(lambda p: p != "", set(list_of_generated_passwords))),
            key=lambda el: len(el),
        )

        # Compute all the combinations of the generated passwords with additional words
        if len(additional_words) > 0:
            list_of_generated_passwords = [
                concat_strings([pwd, *additional_words])
                for pwd in list_of_generated_passwords
            ]
            list_of_generated_passwords = list(chain(*list_of_generated_passwords))

    return list_of_generated_passwords


def generate_password_from_full_content(
    content: str,
    contain_special_character: bool = False,
    alternate_case: bool = False,
    enhance_password_strength: bool = False,
) -> str:
    """Generate a password from an user's input (a favorite quote, a favorite words, ...) with its full content

    Args:
        content (str): _description_
        contain_special_character (bool, optional): If True, the program will modify to add some special character to the password which may make it harder to remember. Default to False.
        alternate_case (bool, optional): If True, the program will alternate the case of some letters in the password which may make it harder to remember. Default to False.
        enhance_password_strength (bool, optional): If True, the program will make more modification to the original content which may make it harder to remember. Default to False.

    Returns:
        str: password generate from its full content
    """
    # Capitalize the string and remove spaces
    content = content.title().replace(" ", "")

    #  If the quote is less than 8 letters long, add itself to increase the length
    _content = content
    while len(content) < 8:
        content += _content

    # Replace normal letter with numeric/special character, preserve the first letter if it is an alphabetic character
    password = (
        content[0]
        + replace_letter_with_alternative(
            content[1:],
            contain_special_character,
            replace_all=enhance_password_strength,
        )
        if content[0].isalpha()
        else replace_letter_with_alternative(
            content, contain_special_character, replace_all=enhance_password_strength
        )
    )

    # Alternate case in the generated password
    password = password if not alternate_case else alternate_case_in_string(password)

    return password


def generate_password_from_content_simplified(
    content: str,
    contain_special_character: bool = False,
    alternate_case: bool = False,
    enhance_password_strength: bool = False,
) -> str:
    """Generate a password from an user's sentence, favorite quote

    Args:
        content (str): a sentence
        contain_special_character (bool, optional): If True, the program will modify to add some special character to the password which may make it harder to remember. Default to False.
        alternate_case (bool, optional): If True, the program will alternate the case of some letters in the password which may make it harder to remember. Default to False.
        enhance_password_strength (bool, optional): If True, the program will make more modification to the original content which may make it harder to remember. Default to False.

    Returns:
        str: _description_
    """

    # Extract only the first letter of each word
    simplified_content = "".join([word[0] for word in content.split()])

    # If the content, is too short to simplified, return an empty string
    if len(simplified_content) < 3:
        return ""

    # Replace normal letter with numeric/special character, but preserve the first letter
    password = (
        simplified_content[0]
        + replace_letter_with_alternative(
            simplified_content[1:],
            contain_special_character,
            replace_all=enhance_password_strength,
        )
        if simplified_content[0].isalpha()
        else replace_letter_with_alternative(
            simplified_content,
            contain_special_character,
            replace_all=enhance_password_strength,
        )
    )

    # Alternate the case of the letters in the password
    password = password if not alternate_case else alternate_case_in_string(password)

    return password


def replace_letter_with_alternative(
    s: str,
    contain_special_character: bool = False,
    replace_all: bool = False,
) -> str:
    """Replace original characters in a string with numeric or suitable special characters. By default, only the first instance of a character that has a replacement is replaced.

    Args:
        s (str): original string
        contain_special_character (bool, optional): if True, the function will include special characters in the replacements. Defaults to False.
        replace_all (bool, optional): if True, all instances of a character that has a replacement will be replace. Defaults to False.

    Returns:
        str: the modified string
    """

    modified_string = list(s)
    replacements = (
        NUMERIC_CHARACTERS_FOR_LETTER_REPLACEMENT
        if not contain_special_character
        else {
            **NUMERIC_CHARACTERS_FOR_LETTER_REPLACEMENT,
            **SPECIAL_CHARACTERS_FOR_LETTER_REPLACEMENT,
        }
    )

    replaced_chars = set()  # Keep track of which characters have been replaced
    for i, char in enumerate(s):
        if (
            char in replacements
            and modified_string[i] == char
            and char not in replaced_chars
        ):
            modified_string[i] = replacements[char]

            if not replace_all:
                replaced_chars.add(char)

    return "".join(modified_string)


def avoid_common_word_and_pwd(password: str) -> str:
    """Replace the common word/password substring with another random substring

    Args:
        password (str):

    Returns:
        str: password without common words/passwords
    """
    common_pwd = validate_with_common_passwords(password)
    common_word = validate_with_common_words(password)

    if common_pwd is None and common_word is None:
        return password

    print("common ...")
    if common_pwd == common_word:
        replace_str = generate_new_str(common_pwd)
        password = password.replace(common_pwd, replace_str)

    # Replace both substring
    if common_pwd is not None:
        replace_str = generate_new_str(common_pwd)
        password = password.replace(common_pwd, replace_str)

    if common_word is not None:
        replace_str = generate_new_str(common_word)
        password = password.replace(common_word, replace_str)

    return password


# ********* Password Validation ********* #


def validate_password(
    password: str,
    username: str = None,
    check_common_pwd: bool = False,
    check_common_words: bool = False,
) -> tuple[dict, int]:
    """Analyze the strength of password based on Microsoft password rules.

    Args:
        password (str)
        username (str, optional): If given, will be used to check with password.
        check_common_pwd (bool, optional): If True, a million common passwords will be loaded to compare with the given password. Defaults to False.
        check_common_words (bool, optional): If True, 10k common words will be loaded to compare with the given password. Defaults to False.

    Returns:
        tuple[dict, int]: Analyzed results and the password strength
    """

    password_strength = 0

    results = {
        "short_password": len(password) <= 8,
        "has_numerical_character": False,
        "has_uppercase_letter": False,
        "has_lowercase_letter": False,
        "has_special_character": False,
        "has_repetitive_substring": detect_repeated_substring(password),
    }

    # Check for required characters in password
    for character in password:
        if character.isdigit():
            results["has_numerical_character"] = True

        if character.isupper():
            results["has_uppercase_letter"] = True

        if character.islower():
            results["has_lowercase_letter"] = True

        if character in SPECIAL_CHARACTERS:
            results["has_special_character"] = True

    # Check if password and username has string/word that in common
    if username:
        results.setdefault("contains_username", None)

        common_substr = longest_common_substring(
            username, password, case_sensitive=False
        )
        if len(common_substr) >= 3:
            results["contains_username"] = common_substr

    # Check for common passwords
    if check_common_pwd:
        common_pwd = validate_with_common_passwords(password)
        results.setdefault("is_common_pwd", common_pwd)

    # Check for common words
    if check_common_words:
        common_word = validate_with_common_words(password)
        results.setdefault("has_common_word", common_word)

    # Calculate password strength
    for feature in PASSWORD_GOOD_FEATURES:
        if results.get(feature):
            password_strength += 1

    for feature in PASSWORD_BAD_FEATURES:
        if feature in results.keys() and not results.get(feature):
            password_strength += 1

    return results, password_strength


def load_common_passwords() -> list[str]:
    """Load 1 mil common passwords from file for validation

    Returns:
        list: List of 1 mil passwords
    """
    with open("./data/10_mil_common_pwd.txt", "r") as f:
        data = map(lambda x: x.rstrip(), f.readlines())

    return list(data)


def validate_with_common_passwords(password: str) -> Union[str, None]:
    """Check if the given password is the same with one of the most common used passwords in the world

    Args:
        password (str)

    Returns:
        Union[str, None]:
            - Return a string as a match password.
            - Return None if there is no password match.
    """

    common_pwd = [pwd for pwd in load_common_passwords() if len(pwd) > 3]
    for pwd in common_pwd:
        if pwd.lower() == password.lower():
            return pwd

    return None


def load_common_words() -> list[str]:
    """Load 10 k common used words from Google for validation

    Returns:
        list: List of 10 k common used words
    """
    with open("./data/10_k_common_password_words.txt", "r") as f:
        data = map(lambda x: x.rstrip(), f.readlines())

    return list(data)


def validate_with_common_words(password: str) -> Union[str, None]:
    """Check if the given password is the same or has similarity with one of the most common used words in the world

    Args:
        password (str)

    Returns:
        Union[str, None]:
            - Return a string as a match word.
            - Return None if there is no word match.
    """

    common_pwd = [word for word in load_common_words() if len(word) > 3]
    for pwd in common_pwd:
        if pwd in password:
            return pwd

    return None
