import unittest
from unidecode import unidecode
from qb_gen.Password import (
    generate_password_from_user_input,
    generate_password_from_full_content,
    generate_password_from_content_simplified,
)
from qb_gen.constants import (
    UPPERCASE_LETTERS,
    LOWERCASE_LETTERS,
    NUMERIC_CHARACTERS_FOR_LETTER_REPLACEMENT,
    SPECIAL_CHARACTERS_FOR_LETTER_REPLACEMENT,
    SUITABLE_SPECIAL_CHARACTERS,
)

QUOTE_1 = "The future belongs to those who believe in the beauty of their dreams"
QUOTE_1_FROM_FULL_CONTENT = "thefuturebelongstothosewhobelieveinthebeautyoftheirdreams"
QUOTE_1_SIMPLIFIED = "tfbttwbitbotd"

QUOTE_2 = "A person who never made a mistake never tried anything new"
QUOTE_2_FROM_FULL_CONTENT = "apersonwhonevermadeamistakenevertriedanythingnew"
QUOTE_2_SIMPLIFIED = "apwnmamntan"

QUOTE_3 = "The way to get started is to quit talking and begin doing. - Walt Disney"
QUOTE_3_FROM_FULL_CONTENT = "thewaytogetstartedistoquittalkingandbegindoing.-waltdisney"
QUOTE_3_SIMPLIFIED = "twtgsitqtabd-wd"

QUOTE_4 = unidecode("Cố gắng là cách duy nhất để thành công. - Thomas Edison")
QUOTE_4_FROM_FULL_CONTENT = "coganglacachduynhatdethanhcong.-thomasedison"
QUOTE_4_SIMPLIFIED = "cglcdndtc-te"

QUOTE_5 = "I love you"
QUOTE_5_FROM_FULL_CONTENT = "iloveyou"
QUOTE_5_SIMPLIFIED = "ily"

WORD_1 = "Chelsea"
WORD_1_DOUBLE = "chelseachelsea"

WORD_2 = "Curry"
WORD_2_DOUBLE = "currycurry"

REPLACEMENTS = {
    **NUMERIC_CHARACTERS_FOR_LETTER_REPLACEMENT,
    **SPECIAL_CHARACTERS_FOR_LETTER_REPLACEMENT,
}


def get_key(dictionary: dict, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None


class TestGeneratePasswordUserInput(unittest.TestCase):
    def _compare_result(self, generated_password: str, expected_str: str):
        generated_password = generated_password.lower()
        expected_str = expected_str.lower()

        for index in range(len(generated_password)):
            if generated_password[index] != expected_str[index]:
                replacement = get_key(REPLACEMENTS, generated_password[index])

                if replacement is None:
                    return False

                if replacement.lower() != expected_str[index]:
                    print(
                        "\n",
                        index,
                        generated_password[index],
                        replacement,
                        expected_str[index],
                    )
                    return False

        return True

    def test_with_full_content(self):
        # Test case #1
        generated_password = generate_password_from_full_content(QUOTE_1)

        self.assertEqual(
            len(generated_password),
            len(QUOTE_1_FROM_FULL_CONTENT),
            msg="Password length should be as expected #1.",
        )
        self.assertTrue(
            self._compare_result(
                generated_password,
                QUOTE_1_FROM_FULL_CONTENT,
            ),
            msg="Password should generate depends on the original content #1.",
        )

        # Test case #2
        generated_password = generate_password_from_full_content(QUOTE_2)

        self.assertEqual(
            len(generated_password),
            len(QUOTE_2_FROM_FULL_CONTENT),
            msg="Password length should be as expected #2.",
        )
        self.assertTrue(
            self._compare_result(
                generated_password,
                QUOTE_2_FROM_FULL_CONTENT,
            ),
            msg="Password should generate depends on the original content #2.",
        )

        # Test case #3
        generated_password = generate_password_from_full_content(QUOTE_3)

        self.assertEqual(
            len(generated_password),
            len(QUOTE_3_FROM_FULL_CONTENT),
            msg="Password length should be as expected #3.",
        )
        self.assertTrue(
            self._compare_result(
                generated_password,
                QUOTE_3_FROM_FULL_CONTENT,
            ),
            msg="Password should generate depends on the original content #3.",
        )

        # Test case #4
        generated_password = generate_password_from_full_content(QUOTE_4)

        self.assertEqual(
            len(generated_password),
            len(QUOTE_4_FROM_FULL_CONTENT),
            msg="Password length should be as expected #4.",
        )
        self.assertTrue(
            self._compare_result(
                generated_password,
                QUOTE_4_FROM_FULL_CONTENT,
            ),
            msg="Password should generate depends on the original content #4.",
        )

        # Test case #5
        generated_password = generate_password_from_full_content(QUOTE_5)

        self.assertEqual(
            len(generated_password),
            len(QUOTE_5_FROM_FULL_CONTENT),
            msg="Password length should be as expected #5.",
        )
        self.assertTrue(
            self._compare_result(
                generated_password,
                QUOTE_5_FROM_FULL_CONTENT,
            ),
            msg="Password should generate depends on the original content #5.",
        )

        # Test case #6
        generated_password = generate_password_from_full_content(WORD_1)

        self.assertEqual(
            len(generated_password),
            len(WORD_1_DOUBLE),
            msg="Password length should be as expected #6.",
        )
        self.assertTrue(
            self._compare_result(
                generated_password,
                WORD_1_DOUBLE,
            ),
            msg="Password should generate depends on the original content #6.",
        )

        # Test case #7
        generated_password = generate_password_from_full_content(WORD_2)

        self.assertEqual(
            len(generated_password),
            len(WORD_2_DOUBLE),
            msg="Password length should be as expected #7.",
        )
        self.assertTrue(
            self._compare_result(
                generated_password,
                WORD_2_DOUBLE,
            ),
            msg="Password should generate depends on the original content #7.",
        )

    def test_full_content_features(self):
        # Contain special character
        for index, case in enumerate([QUOTE_1, QUOTE_3, WORD_1]):
            generated_password = generate_password_from_full_content(
                case, contain_special_character=True
            )
            self.assertTrue(
                any(char in SUITABLE_SPECIAL_CHARACTERS for char in generated_password),
                msg=f"Password should contain suitable special characters #{index + 1}.",
            )

        # Not contain special character
        for index, case in enumerate([QUOTE_2, QUOTE_4, WORD_2]):
            generated_password = generate_password_from_full_content(
                case, contain_special_character=False
            )
            self.assertTrue(
                any(
                    not char in SUITABLE_SPECIAL_CHARACTERS
                    for char in generated_password
                ),
                msg=f"Password should not contain any special characters #{index + 4}.",
            )

        # Alternate case in a string
        for index, case in enumerate([QUOTE_1, QUOTE_2, QUOTE_3, WORD_1, WORD_2]):
            generated_password = generate_password_from_full_content(
                case, alternate_case=True
            )

            has_uppercase = any(
                char in UPPERCASE_LETTERS for char in generated_password
            )
            has_lowercase = any(
                char in LOWERCASE_LETTERS for char in generated_password
            )

            self.assertTrue(
                all([has_uppercase, has_lowercase]),
                msg=f"Password should contain both lowercase and uppercase letters as the cases are alternated #{index + 7}.",
            )

    def test_with_content_simplified(self):
        # Test case #1
        generated_password = generate_password_from_content_simplified(QUOTE_1)

        self.assertEqual(
            len(generated_password),
            len(QUOTE_1_SIMPLIFIED),
            msg="Password length should be as expected #1.",
        )
        self.assertTrue(
            self._compare_result(
                generated_password,
                QUOTE_1_SIMPLIFIED,
            ),
            msg="Password should generate depends on the original content #1.",
        )

        # Test case #2
        generated_password = generate_password_from_content_simplified(QUOTE_2)

        self.assertEqual(
            len(generated_password),
            len(QUOTE_2_SIMPLIFIED),
            msg="Password length should be as expected #2.",
        )
        self.assertTrue(
            self._compare_result(
                generated_password,
                QUOTE_2_SIMPLIFIED,
            ),
            msg="Password should generate depends on the original content #2.",
        )

        # Test case #3
        generated_password = generate_password_from_content_simplified(QUOTE_3)

        self.assertEqual(
            len(generated_password),
            len(QUOTE_3_SIMPLIFIED),
            msg="Password length should be as expected #3.",
        )
        self.assertTrue(
            self._compare_result(
                generated_password,
                QUOTE_3_SIMPLIFIED,
            ),
            msg="Password should generate depends on the original content #3.",
        )

        # Test case #4
        generated_password = generate_password_from_content_simplified(QUOTE_4)

        self.assertEqual(
            len(generated_password),
            len(QUOTE_4_SIMPLIFIED),
            msg="Password length should be as expected #4.",
        )
        self.assertTrue(
            self._compare_result(
                generated_password,
                QUOTE_4_SIMPLIFIED,
            ),
            msg="Password should generate depends on the original content #4.",
        )

        # Test case #5
        generated_password = generate_password_from_content_simplified(QUOTE_5)

        self.assertEqual(
            len(generated_password),
            len(QUOTE_5_SIMPLIFIED),
            msg="Password length should be as expected #5.",
        )
        self.assertTrue(
            self._compare_result(
                generated_password,
                QUOTE_5_SIMPLIFIED,
            ),
            msg="Password should generate depends on the original content #5.",
        )

        # Other test cases (inefficient length)
        for index, case in enumerate([WORD_1, WORD_2]):
            generated_password = generate_password_from_content_simplified(case)

            self.assertEqual(
                len(generated_password),
                0,
                msg=f"Password length should be as zero because of inefficient length #{index + 6}.",
            )

    def test_simplified_features(self):
        # Contain special character
        for index, case in enumerate([QUOTE_2, QUOTE_3, QUOTE_4]):
            generated_password = generate_password_from_content_simplified(
                case, contain_special_character=True
            )
            self.assertTrue(
                any(char in SUITABLE_SPECIAL_CHARACTERS for char in generated_password),
                msg=f"Password should contain suitable special characters #{index + 1}.",
            )

        # Not contain special character
        for index, case in enumerate([QUOTE_2, QUOTE_3, QUOTE_4]):
            generated_password = generate_password_from_content_simplified(
                case, contain_special_character=False
            )
            self.assertTrue(
                any(
                    not char in SUITABLE_SPECIAL_CHARACTERS
                    for char in generated_password
                ),
                msg=f"Password should not contain any special characters #{index + 4}.",
            )

        # Alternate case in a string
        for index, case in enumerate([QUOTE_1, QUOTE_2, QUOTE_3, QUOTE_4]):
            generated_password = generate_password_from_content_simplified(
                case, alternate_case=True
            )

            has_uppercase = any(
                char in UPPERCASE_LETTERS for char in generated_password
            )
            has_lowercase = any(
                char in LOWERCASE_LETTERS for char in generated_password
            )

            self.assertTrue(
                all([has_uppercase, has_lowercase]),
                msg=f"Password should contain both lowercase and uppercase letters as the cases are alternated #{index + 7}.",
            )

    def test_generate_from_user_input(self):
        generated_passwords_1 = generate_password_from_user_input(user_input=QUOTE_1)
        has_simplified_pwd = any(
            (len(pwd) == len(QUOTE_1_SIMPLIFIED)) for pwd in generated_passwords_1
        )
        has_full_content_pwd = any(
            (len(pwd) == len(QUOTE_1_FROM_FULL_CONTENT))
            for pwd in generated_passwords_1
        )
        self.assertTrue(all([has_simplified_pwd, has_full_content_pwd]))

        generated_passwords_2 = generate_password_from_user_input(user_input=QUOTE_3)
        has_simplified_pwd = any(
            (len(pwd) == len(QUOTE_3_SIMPLIFIED)) for pwd in generated_passwords_2
        )
        has_full_content_pwd = any(
            (len(pwd) == len(QUOTE_3_FROM_FULL_CONTENT))
            for pwd in generated_passwords_2
        )
        self.assertTrue(all([has_simplified_pwd, has_full_content_pwd]))

        generated_passwords_3 = generate_password_from_user_input(user_input=QUOTE_5)
        has_simplified_pwd = any(
            (len(pwd) == len(QUOTE_5_SIMPLIFIED)) for pwd in generated_passwords_3
        )
        has_full_content_pwd = any(
            (len(pwd) == len(QUOTE_5_FROM_FULL_CONTENT))
            for pwd in generated_passwords_3
        )
        self.assertTrue(all([has_simplified_pwd, has_full_content_pwd]))

    def test_generate_from_user_input_with_words(self):
        additional_words = [WORD_1, WORD_2]
        total_length = sum(len(s) for s in additional_words)

        # First example
        generated_passwords_1 = generate_password_from_user_input(
            user_input=QUOTE_1, additional_words=additional_words, all_variants=True
        )
        has_simplified_pwd = any(
            (len(pwd) == len(QUOTE_1_SIMPLIFIED) + total_length)
            for pwd in generated_passwords_1
        )
        has_full_content_pwd = any(
            (len(pwd) == len(QUOTE_1_FROM_FULL_CONTENT) + total_length)
            for pwd in generated_passwords_1
        )
        self.assertTrue(all([has_simplified_pwd, has_full_content_pwd]))
        contain_word_1 = all(WORD_1 in pwd for pwd in generated_passwords_1)
        contain_word_2 = all(WORD_2 in pwd for pwd in generated_passwords_1)
        self.assertTrue(all([contain_word_1, contain_word_2]))

        # Second example
        generated_passwords_2 = generate_password_from_user_input(
            user_input=QUOTE_5, additional_words=additional_words, all_variants=True
        )
        has_simplified_pwd = any(
            (len(pwd) == len(QUOTE_5_SIMPLIFIED) + total_length)
            for pwd in generated_passwords_2
        )
        has_full_content_pwd = any(
            (len(pwd) == len(QUOTE_5_FROM_FULL_CONTENT) + total_length)
            for pwd in generated_passwords_2
        )
        self.assertTrue(all([has_simplified_pwd, has_full_content_pwd]))
        contain_word_1 = all(WORD_1 in pwd for pwd in generated_passwords_2)
        contain_word_2 = all(WORD_2 in pwd for pwd in generated_passwords_2)
        self.assertTrue(all([contain_word_1, contain_word_2]))
