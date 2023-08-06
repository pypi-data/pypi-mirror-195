import unittest
from unidecode import unidecode
from random import randint
from qb_gen.Password import generate_password, validate_password
from qb_gen.constants import (
    SUITABLE_SPECIAL_CHARACTERS,
    SPECIAL_CHARACTERS,
    UPPERCASE_LETTERS,
    LOWERCASE_LETTERS,
    NUMERIC_LETTERS,
)


class TestGeneratePassword(unittest.TestCase):
    def _check_password_length(self, password: str, length: int):
        self.assertEqual(
            len(password),
            length,
            msg=f"Password should be length {length}.",
        )

    def test_invalid_password_length(self):
        # Test that the function raises an exception for invalid password length
        with self.assertRaises(Exception):
            generate_password(-1)

    def test_contain_special_characters(self):
        # Test that the generated passwords contain special characters if requested
        for _ in range(3):
            pwd = generate_password(20, contain_special_character=True)
            self.assertTrue(
                any(char in SUITABLE_SPECIAL_CHARACTERS for char in pwd),
                msg="Password should contain suitable special characters.",
            )
            self._check_password_length(pwd, 20)

        # Test that the generated passwords do not contain special characters if not requested
        for _ in range(3):
            pwd = generate_password(20, contain_special_character=False)
            self.assertFalse(
                any(char in SPECIAL_CHARACTERS for char in pwd),
                msg="Password should not contain any special character.",
            )
            self._check_password_length(pwd, 20)

    def test_generate_with_efficient_length(self):
        # Test that the password has the correct structure (lowercase, uppercase, numeric)
        for _ in range(5):
            random_length = randint(12, 30)
            pwd = generate_password(random_length)

            _, strength = validate_password(
                pwd, check_common_pwd=True, check_common_words=True
            )

            self.assertGreaterEqual(strength, 7)
            self._check_password_length(pwd, random_length)

    def test_generate_with_inefficient_length(self):
        # Password with length 1, 2 and 3
        for length in [1, 2, 3]:
            pwd = generate_password(length)

            self.assertTrue(
                pwd.isalpha(),
                msg=f"Password with length {length} should be an alphabetic character.",
            )
            self._check_password_length(pwd, length)

        # Password with length between 4 and 8
        for length in range(4, 9):
            pwd = generate_password(length)

            has_uppercase = bool(set(pwd).intersection(set(UPPERCASE_LETTERS)))
            has_lowercase = bool(set(pwd).intersection(set(LOWERCASE_LETTERS)))
            has_num = bool(set(pwd).intersection(set(NUMERIC_LETTERS)))
            has_special_character = bool(
                set(pwd).intersection(set(SUITABLE_SPECIAL_CHARACTERS))
            )

            self.assertTrue(
                all([has_uppercase, has_lowercase, has_num, has_special_character])
            )
            self._check_password_length(pwd, length)


if __name__ == "__main__":
    unittest.main()
