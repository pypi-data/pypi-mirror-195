<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
    <a href="https://github.com/NgoQuocBao1010/QB-generator">
        <img src="./images/logo.png" alt="Logo" width="60%">
    </a>
  <p align="center">
    Password validator and generator CLI tool.
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

My project is a CLI application that aims to validate the strength of passwords, generate random passwords, and create passwords based on user inputs. The idea for this project was inspired by a similar project on Kaggle, which can be found at [here](https://www.kaggle.com/code/kingabzpro/finding-the-bad-password). The password generation and validation functions of this application are based on the [Microsoft Password Requirements](https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/password-must-meet-complexity-requirements).

<p align="right">(<a href="#top">back to top</a>)</p>

## Getting Started

This is an example of how you may give instructions on setting up the project locally.

#### Setting Up Environment

```
    Python 3.9.13
    OS: Linux or MacOS
```

```markdown
    NOTES
    ⚠️ Commands/Scripts for this project are wrote for Linux-based OS. They may not work on Windows machines.
```

### Installation

1. Clone the repo and change directory to that folder

    ```sh
    git clone https://github.com/NgoQuocBao1010/QB-generator.git
    ```

1. Install all project dependencies

    ```bash
    pip install -r requirements.txt
    ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
<div id="usage"></div>
<br/>

## Usage

1. CLI application's usage

    | Command         | Description                                                                                 |
    | --------------- | ------------------------------------------------------------------------------------------- |
    | `validate`      | Validate password according to Microsoft rules.                                             |
    | `generate`      | Generate a strong password.                                                                 |
    | `generate-from` | Generate a password (or multiple passwords) based on a phrase or word provided by the user. |

    #### `validate` command

    | Argument            | Option | Description                                                   |
    | ------------------- | ------ | ------------------------------------------------------------- |
    | `password`          | `ARG`  | The password to validate.                                     |
    | `--username`, `-u`  | `OPT`  | The username correspond to password for extra validation.     |
    | `--common-pwd`      | `OPT`  | Check if the password is similar to other common passwords    |
    | `--common-words`    | `OPT`  | Check if the password contains most common used words         |
    | `--check-all`, `-y` | `OPT`  | Shortcut to check for both common passwords and common words. |
    | `--ignore-warnings` | `OPT`  | Ignore all warnings.                                          |

    #### `generate` command

    | Argument              | Option | Description                                               |
    | --------------------- | ------ | --------------------------------------------------------- |
    | `--length`, `-l`      | `OPT`  | Length for the generated password. Should be more than 8. |
    | `--special-character` | `OPT`  | If True, password will contains special characters.       |
    | `--no-copy`           | `OPT`  | Avoid save password to clipboard.                         |

    #### `generate-from` command

    | Argument           | Option | Description                                                                 |
    | ------------------ | ------ | --------------------------------------------------------------------------- |
    | `user_input`       | `ARG`  | A quote or words given by the user.                                         |
    | `--add`            | `OPT`  | Additional words to add to the generated password without any modification. |
    | `--all`, `-a`      | `OPT`  | Return all the possible generated passwords.                                |
    | `--pwd-validation` | `OPT`  | Turn on password strength analysis.                                         |
    | `--max-strength`   | `OPT`  | Only return the strongest password                                          |

1. Programmatically usage

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

-   [Logo marker](https://www4.flamingtext.com/) for this project.
-   This awesome README template is from [Best README Template](https://github.com/othneildrew/Best-README-Template).

<p align="right">(<a href="#top">back to top</a>)</p>
