import string

# * Password Characters
UPPERCASE_LETTERS = string.ascii_uppercase
LOWERCASE_LETTERS = string.ascii_lowercase
NUMERIC_LETTERS = string.digits
SPECIAL_CHARACTERS = string.punctuation
UNSUITABLE_SPECIAL_CHARACTER = "".join(
    ["'", '"', "\\", "<", ">", "&", "#", "%", "^", "~"]
)
SUITABLE_SPECIAL_CHARACTERS = "".join(
    filter(lambda char: char not in UNSUITABLE_SPECIAL_CHARACTER, SPECIAL_CHARACTERS)
)
SPECIAL_CHARACTERS_FOR_LETTER_REPLACEMENT = {
    "a": "@",
    "A": "@",
    "C": "(",
    "c": "(",
    "s": "$",
    "S": "$",
    "1": "!",
    "2": "?",
}
NUMERIC_CHARACTERS_FOR_LETTER_REPLACEMENT = {
    "o": "0",
    "O": "0",
    "i": "1",
    "I": "1",
    "z": "2",
    "Z": "2",
    "e": "3",
    "B": "8",
}


# * Password criteria
PASSWORD_GOOD_FEATURES = (
    "has_numerical_character",
    "has_uppercase_letter",
    "has_lowercase_letter",
    "has_special_character",
)
PASSWORD_BAD_FEATURES = (
    "short_password",
    "has_repetitive_substring",
    "is_common_pwd",
    "has_common_word",
    "contains_username",
)
PASSWORD_VALIDATION_CRITERIA = {
    "short_password": "Password length should be greater than 8",
    "is_common_pwd": "Password should not have pawned or publicly leaked passwords",
    "has_common_word": "Password should not have Google most common word",
    "contains_username": "Password should not contain username",
    "has_repetitive_substring": "Password should not have repetitive character",
    "has_numerical_character": "Password should have at least one numerical",
    "has_uppercase_letter": "Password should have at least one uppercase letter",
    "has_lowercase_letter": "Password should have at least one lowercase letter",
    "has_special_character": "Password should have at least one of the special characters",
}
