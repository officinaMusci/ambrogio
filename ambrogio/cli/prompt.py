from typing import Any, Optional

import inquirer


class Prompt:
    """
    Prompt the user with interactive command line interfaces.
    """

    @classmethod
    def confirm(cls, message: str, **kwargs) -> Optional[bool]:
        kwargs = {'message': message, **kwargs}
        return cls._convert_to_inquirer('confirm', **kwargs)

    @classmethod
    def text(cls, message: str, **kwargs) -> Optional[str]:
        kwargs = {'message': message, **kwargs}
        return cls._convert_to_inquirer('text', **kwargs)

    @classmethod
    def editor(cls, message: str, **kwargs) -> Optional[str]:
        kwargs = {'message': message, **kwargs}
        return cls._convert_to_inquirer('editor', **kwargs)

    @classmethod
    def path(cls, message: str, **kwargs) -> Optional[str]:
        kwargs = {'message': message, **kwargs}
        return cls._convert_to_inquirer('path', **kwargs)

    @classmethod
    def password(cls, message: str, **kwargs) -> Optional[str]:
        kwargs = {'message': message, **kwargs}
        return cls._convert_to_inquirer('password', **kwargs)

    @classmethod
    def checkbox(cls, message: str, choices: list, **kwargs) -> Any:
        kwargs = {'message': message, 'choices': choices, **kwargs}
        return cls._convert_to_inquirer('checkbox', **kwargs)

    @classmethod
    def list(cls, message: str, choices: list, **kwargs) -> Any:
        kwargs = {'message': message, 'choices': choices, **kwargs}
        return cls._convert_to_inquirer('list', **kwargs)

    @staticmethod
    def _convert_to_inquirer(method:str, **kwargs):
        questions = [
            getattr(inquirer, method.capitalize())('answer', **kwargs)
        ]

        result = inquirer.prompt(questions)

        return result['answer'] if result else None