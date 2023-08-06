from rich import print
from qb_gen.constants import PASSWORD_VALIDATION_CRITERIA

COLORS = {"ORANGE": "#f59105", "LIGHT GREEN": "#05f58d"}


def display_password_criteria(results: dict) -> None:
    """Display the analyze results of the password to the terminal

    Args:
        results (dict): The analyze results of the password validation
    """

    status_icon = lambda status: "✅" if status else "❌"
    status_color = lambda status: "green" if status else "red"
    display_criteria = lambda crit, status: print(
        "{icon}[bold][{color}] {criteria} [{color}][bold]".format(
            icon=status_icon(status),
            color=status_color(status),
            criteria=PASSWORD_VALIDATION_CRITERIA.get(crit),
        )
    )

    display_criteria("short_password", not results.get("short_password"))
    display_criteria(
        "has_repetitive_substring", not results.get("has_repetitive_substring")
    )
    display_criteria("has_numerical_character", results.get("has_numerical_character"))
    display_criteria("has_uppercase_letter", results.get("has_uppercase_letter"))
    display_criteria("has_lowercase_letter", results.get("has_lowercase_letter"))
    display_criteria("has_special_character", results.get("has_special_character"))

    if "has_common_word" in results.keys():
        display_criteria("has_common_word", not results.get("has_common_word"))

    if "is_common_pwd" in results.keys():
        display_criteria("is_common_pwd", not results.get("is_common_pwd"))

    if "contains_username" in results.keys():
        display_criteria("contains_username", not results.get("contains_username"))


def display_warning(text: str, add_trail_newline: bool = False, *args) -> None:
    """Display a warning in terminal

    Args:
        text (str): Warning text
        add_trail_newline (bool, optional): If True, add another newline after the content. Default to False.
    """
    print(
        f"⚠️ [bold yellow] {text} [/bold yellow]" + ("\n" if add_trail_newline else "")
    )


def display_list(list_content: list[str], add_trail_newline: bool = False) -> None:
    """Display a list of text to terminal

    Args:
        list_content (list[str]): list of text
        add_trail_newline (bool, optional): If True, add another newline after the content. Defaults to False.
    """

    for i, text in enumerate(list_content):
        print(f"{i + 1}. {text}")

    if add_trail_newline:
        print("")


def identify_password_strength(pwd_strength: int) -> tuple[str]:
    """Give a color depend on the strength of a given password

    Args:
        pwd_strength (int): password's strength

    Returns:
        tuple[str]: (color for the password's strength, status of the password's strength)
    """
    if not 1 <= pwd_strength <= 9:
        raise Exception("Invalid password strength.")

    if pwd_strength < 4:
        return ("weak", "red")
    elif pwd_strength == 4 or pwd_strength == 5:
        return ("medium", COLORS.get("ORANGE"))
    elif 5 < pwd_strength < 8:
        return ("good", "green")
    elif pwd_strength == 8 or pwd_strength == 9:
        return ("excellent", COLORS.get("LIGHT GREEN"))
