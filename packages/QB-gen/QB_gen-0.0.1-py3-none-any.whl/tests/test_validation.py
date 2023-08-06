import unittest
from qb_gen.Password import (
    validate_password,
)
from qb_gen.constants import PASSWORD_VALIDATION_CRITERIA

REQUIRED_CRITERIA = set(
    [
        crit
        for crit in PASSWORD_VALIDATION_CRITERIA.keys()
        if crit
        not in [
            "contains_username",
            "is_common_pwd",
            "has_common_word",
        ]
    ]
)


class PasswordValidationTestClass(unittest.TestCase):
    def _check_validation_output(self, results: dict, strength: int):
        # Type checking
        self.assertIsInstance(
            results,
            dict,
            "Return a dictionary as an analyzed results of the password validation.",
        )
        self.assertIsInstance(
            strength, int, "Return an integer as a password strength."
        )

        # Check for required criteria
        results_criteria = set(results.keys())
        self.assertTrue(
            results_criteria.issuperset(REQUIRED_CRITERIA),
            msg="Results contain required criteria",
        )

    def test_password_length(self):
        # Test password with length less than 8 characters
        short_passwords = [
            "1234",
            "abc",
            "qwerty",
            "test",
            "password",
            "letmein",
            "monkey",
            "sunshine",
            "iloveyou",
            "secret",
        ]
        result1 = [
            validate_password(pwd)[0].get("short_password") for pwd in short_passwords
        ]
        self.assertTrue(all(result1), msg="Password should be short")

        # Test password with length greater than 8 characters
        long_passwords = [
            "ThisIsAVeryLongPassword!",
            "SuperSecurePassword123456",
            "SecurePassword123456!",
        ]
        result2 = [
            validate_password(pwd)[0].get("short_password") for pwd in long_passwords
        ]
        self.assertFalse(all(result2), msg="Password should not be short")

    def test_password_character_types(self):
        # Test password with numerical character
        passwords_with_num = [
            "1234",
            "abc123",
            "a1bcd",
        ]
        result1 = [
            validate_password(pwd)[0].get("has_numerical_character")
            for pwd in passwords_with_num
        ]
        self.assertTrue(
            all(result1), msg="Password should contain a numerical character"
        )

        # Test password with uppercase letter
        passwords_with_uppercase = [
            "ABCabc1",
            "ZZ123",
        ]
        result2 = [
            validate_password(pwd)[0].get("has_uppercase_letter")
            for pwd in passwords_with_uppercase
        ]
        self.assertTrue(all(result2), msg="Password should contain an uppercase letter")

        # Test password with lowercase letter
        passwords_with_lowercase = [
            "ABCabc1",
            "hh123",
        ]
        result3 = [
            validate_password(pwd)[0].get("has_lowercase_letter")
            for pwd in passwords_with_lowercase
        ]
        self.assertTrue(all(result3), msg="Password should contain an lowercase letter")

        # Test password with special character
        passwords_with_special = [
            "ABC@bc1",
            "&*()",
        ]
        result4 = [
            validate_password(pwd)[0].get("has_special_character")
            for pwd in passwords_with_special
        ]
        self.assertTrue(all(result4), msg="Password should contain a special character")

    def test_contains_username(self):
        # Test passwords contains part of usernames
        passwords = ["john12122000", "brad33", "steph30"]
        usernames = ["JohnDoe", "Bradley Cooper", "StephCurry"]
        result1 = [
            validate_password(pwd, username=usr)[0].get("contains_username")
            for pwd, usr in zip(passwords, usernames)
        ]
        self.assertTrue(
            all(result1), msg="Password should contain part of the username"
        )

        # Test passwords does not contain usernames
        passwords = ["E;Ujx7EhqL", "n(38xcsrK/", "K/Lhpw{I09"]
        usernames = ["JohnDoe", "Bradley Cooper", "StephCurry"]
        result2 = [
            not bool(validate_password(pwd, username=usr)[0].get("contains_username"))
            for pwd, usr in zip(passwords, usernames)
        ]
        self.assertTrue(
            all(result2), msg="Password should not contain part of the username"
        )

    def test_consecutive_repetitive_characters(self):
        # Test password contains consecutive repetitive substring
        passwords_with_rep = [
            "1111",
            "aaaa123",
            "John123123123",
        ]
        rep_substrings = ["1", "a", "123"]
        result1 = [
            validate_password(pwd)[0].get("has_repetitive_substring") == substring
            for pwd, substring in zip(passwords_with_rep, rep_substrings)
        ]
        self.assertTrue(
            all(result1), msg="Password should contain repetitive substring"
        )

        # Test password does not contain consecutive repetitive substring
        password_without_rep = [
            "n9:oSwv6ML",
            "secret",
        ]
        result2 = [
            not bool(validate_password(pwd)[0].get("has_repetitive_substring"))
            for pwd in password_without_rep
        ]
        self.assertTrue(
            all(result2), msg="Password should not contain repetitive substring"
        )

    def test_password_commonality(self):
        # Test passwords contain common word
        common_words = [
            "test",
            "password",
            "chelsea",
        ]
        result1 = [
            validate_password(pwd, check_common_words=True)[0].get("has_common_word")
            for pwd in common_words
        ]
        self.assertTrue(all(result1), msg="Password should contain a common word.")

        # Test passwords that are common passwords
        common_passwords = [
            "p@ssw0rd",
            "ILOVEYOU",
            "PORSCHE",
        ]
        result2 = [
            validate_password(pwd, check_common_pwd=True)[0].get("is_common_pwd")
            for pwd in common_passwords
        ]
        self.assertTrue(all(result2), msg="Password should bea common password.")

        # Test password with no commonality
        passwords = [
            "y(dibE7grr",
            "I!OVEY0U_123",
            "P0R$CHE",
        ]

        result3 = [
            validate_password(pwd, check_common_pwd=True, check_common_words=True)[0]
            for pwd in passwords
        ]

        self.assertTrue(
            all([not bool(r.get("has_common_word")) for r in result3]),
            msg="Password should not contain a common word.",
        )
        self.assertTrue(
            all([not bool(r.get("is_common_pwd")) for r in result3]),
            msg="Password should not be a common password.",
        )

    def test_validate_weak_password(self):
        # Test weak password #1
        password = "weak"

        expected_results = {
            # Good features
            "has_numerical_character": False,
            "has_uppercase_letter": False,
            "has_lowercase_letter": True,
            "has_special_character": False,
            # Bad features
            "short_password": True,
            "has_repetitive_substring": None,
        }
        expected_strength = 2

        results, strength = validate_password(password)
        self._check_validation_output(results, strength)
        self.assertEqual(
            results, expected_results, msg="Expected results should be matched #1."
        )
        self.assertEqual(
            strength, expected_strength, msg="Expected strength should be matched #1."
        )

        # Test weak password #2
        password = "1111"

        expected_results = {
            # Good features
            "has_numerical_character": True,
            "has_uppercase_letter": False,
            "has_lowercase_letter": False,
            "has_special_character": False,
            # Bad features
            "short_password": True,
            "has_repetitive_substring": "1",
        }
        expected_strength = 1

        results, strength = validate_password(password)
        self._check_validation_output(results, strength)
        self.assertEqual(
            results, expected_results, msg="Expected results should be matched #2."
        )
        self.assertEqual(
            strength, expected_strength, msg="Expected strength should be matched #2."
        )

        # Test weak password #3
        password = "passuser"
        username = "username"

        expected_results = {
            # Good features
            "has_numerical_character": False,
            "has_uppercase_letter": False,
            "has_lowercase_letter": True,
            "has_special_character": False,
            # Bad features
            "short_password": True,
            "has_repetitive_substring": None,
            "is_common_pwd": "passuser",
            "has_common_word": "user",
            "contains_username": "user",
        }
        expected_strength = 2

        results, strength = validate_password(
            password,
            username=username,
            check_common_pwd="True",
            check_common_words=True,
        )
        self._check_validation_output(results, strength)
        self.assertEqual(
            results, expected_results, msg="Expected results should be matched #3."
        )
        self.assertEqual(
            strength, expected_strength, msg="Expected strength should be matched #3."
        )

    def test_validate_medium_password(self):
        # Test medium password #2
        password = "Passw0rd"

        expected_results = {
            # Good features
            "has_numerical_character": True,
            "has_uppercase_letter": True,
            "has_lowercase_letter": True,
            "has_special_character": False,
            # Bad features
            "short_password": True,
            "has_repetitive_substring": None,
        }
        expected_strength = 4

        results, strength = validate_password(password)
        self._check_validation_output(results, strength)
        self.assertEqual(
            results, expected_results, msg="Expected results should be matched #1."
        )
        self.assertEqual(
            strength, expected_strength, msg="Expected strength should be matched #1."
        )

        # Test medium password #1
        password = "M3d1umPassw0rd2common"

        expected_results = {
            # Good features
            "has_numerical_character": True,
            "has_uppercase_letter": True,
            "has_lowercase_letter": True,
            "has_special_character": False,
            # Bad features
            "short_password": False,
            "has_repetitive_substring": None,
            "is_common_pwd": None,
            "has_common_word": "common",
        }
        expected_strength = 6

        results, strength = validate_password(
            password, check_common_pwd=True, check_common_words=True
        )
        self._check_validation_output(results, strength)
        self.assertEqual(
            results, expected_results, msg="Expected results should be matched #2."
        )
        self.assertEqual(
            strength, expected_strength, msg="Expected strength should be matched #2."
        )

    def test_validate_great_password(self):
        # Test great password #1
        password = "G00dP@ssw0rd1"

        expected_results = {
            # Good features
            "has_numerical_character": True,
            "has_uppercase_letter": True,
            "has_lowercase_letter": True,
            "has_special_character": True,
            # Bad features
            "short_password": False,
            "has_repetitive_substring": None,
        }
        expected_strength = 6

        results, strength = validate_password(password)
        self._check_validation_output(results, strength)
        self.assertEqual(
            results, expected_results, msg="Expected results should be matched #1."
        )
        self.assertEqual(
            strength, expected_strength, msg="Expected strength should be matched #1."
        )

        # Test great password #2
        password = "ibtuP3@TNhqb"

        expected_results = {
            # Good features
            "has_numerical_character": True,
            "has_uppercase_letter": True,
            "has_lowercase_letter": True,
            "has_special_character": True,
            # Bad features
            "short_password": False,
            "has_repetitive_substring": None,
            "is_common_pwd": None,
            "has_common_word": None,
        }
        expected_strength = 8

        results, strength = validate_password(
            password, check_common_pwd=True, check_common_words=True
        )
        self._check_validation_output(results, strength)
        self.assertEqual(
            results, expected_results, msg="Expected results should be matched #2."
        )
        self.assertEqual(
            strength, expected_strength, msg="Expected strength should be matched #2."
        )

        # Test great password #3
        password = "M06wLRctpsyx_WHMwcRv"
        username = "JohnDoe123"

        expected_results = {
            # Good features
            "has_numerical_character": True,
            "has_uppercase_letter": True,
            "has_lowercase_letter": True,
            "has_special_character": True,
            # Bad features
            "short_password": False,
            "has_repetitive_substring": None,
            "contains_username": None,
            "is_common_pwd": None,
            "has_common_word": None,
        }
        expected_strength = 9

        results, strength = validate_password(
            password, username=username, check_common_pwd=True, check_common_words=True
        )
        self._check_validation_output(results, strength)
        self.assertEqual(
            results, expected_results, msg="Expected results should be matched #3."
        )
        self.assertEqual(
            strength, expected_strength, msg="Expected strength should be matched #3."
        )


if __name__ == "__main__":
    unittest.main()
