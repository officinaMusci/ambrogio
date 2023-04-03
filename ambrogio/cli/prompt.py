from typing import Any, Optional
from pathlib import Path
from time import sleep

import inquirer

from ambrogio.utils.threading import pause_event


class Prompt:
    """
    Prompt the user with interactive command line interfaces.
    """

    @classmethod
    def confirm(cls, message: str, **kwargs) -> Optional[bool]:
        """
        Ask the user to confirm something.
        
        :param message: The message to display.
        :param kwargs: Keyword arguments to pass to the prompt.
        
        :return: The user's response.
        """

        kwargs = {'message': message, **kwargs}
        return cls._convert_to_inquirer('confirm', **kwargs)

    @classmethod
    def text(cls, message: str, **kwargs) -> Optional[str]:
        """
        Ask the user to input text.
        
        :param message: The message to display.
        :param kwargs: Keyword arguments to pass to the prompt.
        
        :return: The user's response.
        """

        kwargs = {'message': message, **kwargs}
        return cls._convert_to_inquirer('text', **kwargs)

    @classmethod
    def editor(cls, message: str, **kwargs) -> Optional[str]:
        """
        Ask the user to input text using an editor.
        
        :param message: The message to display.
        :param kwargs: Keyword arguments to pass to the prompt.
        
        :return: The user's response.
        """
        
        kwargs = {'message': message, **kwargs}
        return cls._convert_to_inquirer('editor', **kwargs)

    @classmethod
    def path(cls, message: str, **kwargs) -> Optional[Path]:
        """
        Ask the user to input a path.
        
        :param message: The message to display.
        :param kwargs: Keyword arguments to pass to the prompt.
        
        :return: The user's response.
        """

        if 'default' in kwargs and kwargs['default']:
            kwargs['default'] = str(Path(kwargs['default']).resolve())

        kwargs = {'message': message, **kwargs}
        response = cls._convert_to_inquirer('path', **kwargs)

        return Path(response) if response else None

    @classmethod
    def password(cls, message: str, **kwargs) -> Optional[str]:
        """
        Ask the user to input a password.

        :param message: The message to display.
        :param kwargs: Keyword arguments to pass to the prompt.

        :return: The user's response.
        """

        kwargs = {'message': message, **kwargs}
        return cls._convert_to_inquirer('password', **kwargs)

    @classmethod
    def checkbox(cls, message: str, choices: list, **kwargs) -> Any:
        """
        Ask the user to select one or more options from a list.
        
        :param message: The message to display.
        :param choices: The list of choices.
        :param kwargs: Keyword arguments to pass to the prompt.
        
        :return: The user's response.
        """
        kwargs = {'message': message, 'choices': choices, **kwargs}
        return cls._convert_to_inquirer('checkbox', **kwargs)

    @classmethod
    def list(cls, message: str, choices: list, **kwargs) -> Any:
        """
        Ask the user to select one option from a list.

        :param message: The message to display.
        :param choices: The list of choices.
        :param kwargs: Keyword arguments to pass to the prompt.

        :return: The user's response.
        """
        
        kwargs = {'message': message, 'choices': choices, **kwargs}
        return cls._convert_to_inquirer('list', **kwargs)

    @staticmethod
    def _convert_to_inquirer(method:str, **kwargs):
        """
        Convert the method name to the corresponding inquirer method.

        :param method: The method name.
        :param kwargs: The keyword arguments.

        :return: The result of the inquirer method.

        :raises AttributeError: If the method name is not valid.
        """

        pause_event.set()
        sleep(1/2)

        questions = [
            getattr(inquirer, method.capitalize())('answer', **kwargs)
        ]

        result = inquirer.prompt(questions)

        pause_event.clear()
        sleep(1/2)

        return result['answer'] if result else None