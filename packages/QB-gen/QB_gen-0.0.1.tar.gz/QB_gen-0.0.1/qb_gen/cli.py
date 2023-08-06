from typing import List, Optional

import typer
from rich import print
from rich.console import Console

from qb_gen import WELCOME_SCREEN
from qb_gen.Password import (
    generate_password,
    generate_password_from_user_input,
    validate_password,
)
from qb_gen.utils import copy_to_clipboard
from qb_gen.cli_helpers import (
    display_password_criteria,
    display_warning,
    display_list,
    identify_password_strength,
)
from qb_gen.constants import SUITABLE_SPECIAL_CHARACTERS, UNSUITABLE_SPECIAL_CHARACTER

app = typer.Typer()
console = Console()


def _version_callback(value: bool) -> None:
    if value:
        print(WELCOME_SCREEN)
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


# ** PASSWORD VALIDATION
@app.command(name="validate", rich_help_panel="Validation")
def password_validation(
    password: str = typer.Argument(..., help="The password to validate"),
    username: str = typer.Option(
        "",
        "-u",
        "--username",
        help="The username correspond to password for extra validation",
        prompt="An username for this password for extra validation (optional)",
    ),
    check_for_common_pwd: bool = typer.Option(
        False,
        "--common-pwd",
        help="Check if the password is similar to other common passwords (cost more time to validate).",
    ),
    check_for_common_words: bool = typer.Option(
        False,
        "--common-words",
        help="Check if the password contains most common used words (cost more time to validate).",
    ),
    check_all: bool = typer.Option(
        False,
        "-y",
        "--check-all",
        help="Shortcut to check for both common passwords and common words.",
    ),
    ignore_warnings: bool = typer.Option(
        False,
        "--ignore-warnings",
        help="Ignore all warnings.",
    ),
) -> None:
    """Validate password according to Microsoft rules"""

    if check_all:
        check_for_common_pwd = True
        check_for_common_words = True
    else:
        if not check_for_common_pwd:
            check_for_common_pwd = typer.confirm(
                "Do you want to check if the password is similar to other common passwords? (Could cost more time to validate)"
            )
        if not check_for_common_words:
            check_for_common_words = typer.confirm(
                "Do you want to check if the password contains most common used words? (Could cost more time to validate)"
            )

    (results, password_strength) = validate_password(
        password=password,
        username=username,
        check_common_pwd=check_for_common_pwd,
        check_common_words=check_for_common_words,
    )

    print(f"\nPassword strength: {password_strength}")
    (strength_status, strength_color) = identify_password_strength(password_strength)
    print(
        f"[bold][{strength_color}]___{strength_status.upper()} PASSWORDS___[{strength_color}][bold]\n"
    )

    # Some warnings
    if (
        any([char in UNSUITABLE_SPECIAL_CHARACTER for char in password])
        and not ignore_warnings
    ):
        display_warning(
            "Your password contains some special characters that consider not advisable to use in a password.\nRun 'qb_gen special-characters -i' command for more information.",
            add_trail_newline=True,
        )

    # Echoing information to terminal
    display_password_criteria(results)


# ** PASSWORD GENERATOR
@app.command(name="generate", rich_help_panel="Generator")
def password_generator(
    password_length: int = typer.Option(
        12,
        "-l",
        "--length",
        min=1,
        help="Length for the generated password. Should be more than 8",
        prompt="Length of password",
    ),
    contain_special_character: bool = typer.Option(
        True,
        "--special-character",
        help="If True, password will contains special characters.",
    ),
    copy_password_to_clipboard: bool = typer.Option(
        True,
        "--no-copy",
        help="Avoid save password to clipboard.",
    ),
) -> None:
    """Generated a strong password."""

    password = generate_password(
        length=password_length, contain_special_character=contain_special_character
    )

    print(f"\nGenerated Password: [bold blue]{password}[/bold blue]")

    if copy_password_to_clipboard:
        copy_to_clipboard(password)
        print(f"[italic blue]It has been copied to your clipboard ✨[/italic blue]")

    if len(password) <= 8:
        display_warning(text="Password length should be greater than 8")
    return


@app.command(name="generate-from", rich_help_panel="Generator")
def password_generator_from_user_input(
    user_input: str = typer.Argument(
        ...,
        help="A quote or words given by the user. This may result in a less secure password, but it will be easier to remember.",
    ),
    additional_words: Optional[List[str]] = typer.Option(
        [],
        "--add",
        help="Additional words to add to the generated password without any modification.",
        is_eager=True,
    ),
    all_combinations: bool = typer.Option(
        False,
        "-a",
        "--all",
        is_flag=True,
        flag_value=True,
        help="Return all the possible generated passwords.",
    ),
    password_validation: bool = typer.Option(
        False,
        "--pwd-validation",
        is_flag=True,
        flag_value=True,
        help="Turn on password strength analysis.",
    ),
    max_strength: bool = typer.Option(
        False,
        "--max-strength",
        is_flag=True,
        flag_value=True,
        help="Only return the strongest password (note that the generated password may be difficult to remember).",
    ),
) -> None:
    """Generate a password (or multiple passwords) based on a phrase or word provided by the user. For stronger and more memorable passwords, it is recommended to use a short phrase with around 10 characters. By default, the command will return a list of generated passwords. However, if the '--max-strength' option is used, the it will only return a single password with the highest strength."""

    # * Generate a list of passwords from user input
    if not max_strength:
        passwords = generate_password_from_user_input(
            user_input, additional_words=additional_words, all_variants=all_combinations
        )

        # Passwords validation
        password_display_texts = []
        with console.status(
            "[i blue]Generating passwords from your input...", spinner="monkey"
        ) as _:
            if password_validation:
                for pwd in passwords:
                    # Validate password
                    (_, password_strength) = validate_password(
                        pwd, check_common_pwd=True, check_common_words=True
                    )

                    # Styling the password strength
                    (_, strength_color) = identify_password_strength(password_strength)
                    strength_text = (
                        f"[{strength_color}]{password_strength}[{strength_color}]"
                    )
                    password_display_texts.append(
                        f"[bold blue]{pwd}[/bold blue] \t => password strength 💪: {strength_text}"
                    )
            else:
                password_display_texts = [
                    f"[bold blue]{pwd}[/bold blue]" for pwd in passwords
                ]

        # Displaying ...
        print(f"\nOriginal input: [i blue]{user_input}[/i blue]")
        print(
            ""
            if len(additional_words) == 0
            else f"Additional words: '{', '.join(additional_words)}'\n"
        )
        print("Here are your generated passwords 🔑:")
        display_list(password_display_texts)

    # * Generate one only password with the max strength
    else:
        if all_combinations:
            display_warning(
                "The option [i]-a/--all[/i] is disable when using [i]--max-strength[i]",
            )

        password = generate_password_from_user_input(
            user_input, max_strength, additional_words
        )

        # Displaying ...
        print(f"\nOriginal input: [i blue]'{user_input}'[/i blue]")
        print(
            ""
            if len(additional_words) == 0
            else f"Additional words: '{', '.join(additional_words)}'\n"
        )
        print(f"Here are your generated passwords 🔑: [b blue]{password}[b blue]")

        if password_validation:
            # Validate password
            (_, password_strength) = validate_password(
                password, check_common_pwd=True, check_common_words=True
            )

            # Styling the password strength
            (_, strength_color) = identify_password_strength(password_strength)
            print(
                f"Password strength 💪: [{strength_color}]{password_strength}[{strength_color}]"
            )

    return


# ** DISPLAY INFORMATION
@app.command(name="validation-rule", rich_help_panel="Information")
def display_password_validation_rules():
    """Display all the rules which are used to analyze/calculate the strength of a password."""

    text = """
QB generator CLI evaluates the strength of the password based on Microsoft Password Requirements.
For more information, visit the site: [i b]https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/password-must-meet-complexity-requirements[/i b]

1. Password Length should be greater than 8
2. Password should not have pawned or publicly leaked passwords
3. Password should not have Google most common word
4. Password should not have a username
5. Password should not have repetitive character
6. Password should have at least one numerical
7. Password should have at least one uppercase letter
8. Password should have at least one lowercase letter
9. Password should have at least one of the special characters
    """
    print(text)


@app.command(name="special-characters", rich_help_panel="Information")
def display_special_characters(
    include_unsuitable_characters: bool = typer.Option(
        False,
        "-u",
        "--unsuitable-characters",
        is_flag=True,
        flag_value=True,
        help="Include special characters which are not advisable to include in a password.",
    ),
):
    """Display all special characters used to generate and validate password."""

    print(
        f"Special Characters which are [i blue]advisable[/i blue] for generate and validate passwords: [b blue]{SUITABLE_SPECIAL_CHARACTERS}[/b blue]\n",
    )

    if include_unsuitable_characters:
        print(
            f"Special Characters which are not [i yellow]advisable[/i yellow] to include in a password: [b yellow]{UNSUITABLE_SPECIAL_CHARACTER}[/b yellow]\n",
        )
