import os
import sys
from typing import List, Tuple, Any, Optional, Union, Literal
from pathlib import Path
from time import sleep
from datetime import datetime
import json

import inquirer
from inquirer.themes import Theme, term

from ambrogio.cli.logger import logger
from ambrogio.utils.threading import pause_event, exit_event
from ambrogio.utils.validators import (
    validate_date,
    validate_datetime,
    validate_json
)


def ask_for_interrupt():
    """
    On KeyboardInterrupt, ask the user to confirm interrupting the program.
    """

    confirm = Prompt.confirm(
        'Are you sure you want to interrupt the program?',
        default=True
    )

    if confirm:
        exit_event.set()

        logger.warning('Interrupting program...')
        
        sys.exit(0)
    
    else:
        return False


class PromptTheme(Theme):
    def __init__(self):
        super().__init__()
        self.Question.mark_color = term.normal + term.bold
        self.Question.brackets_color = term.normal
        self.Question.default_color = term.normal
        self.Editor.opening_prompt_color = term.normal
        self.Checkbox.selection_color = term.normal + term.bold
        self.Checkbox.selection_icon = ">"
        self.Checkbox.selected_icon = "[X]"
        self.Checkbox.selected_color = term.normal + term.bold
        self.Checkbox.unselected_color = term.normal
        self.Checkbox.unselected_icon = "[ ]"
        self.Checkbox.locked_option_color = term.gray50
        self.List.selection_color = term.normal + term.bold
        self.List.selection_cursor = ">"
        self.List.unselected_color = term.normal


class Prompt:
    """
    Prompt the user with interactive command line interfaces.
    """

    @classmethod
    def confirm(
        cls,
        message: str,
        default: bool = True,
        **kwargs
    ) -> Optional[bool]:
        """
        Ask the user to confirm something.
        
        :param message: The message to display.
        :param default: The default value.
        :param kwargs: Keyword arguments to pass to the prompt.
        
        :return: The user's response.
        """

        return cls._convert_to_inquirer(
            'confirm',
            message = message,
            default = default,
            **kwargs
        )

    @classmethod
    def text(
        cls,
        message: str,
        default: Optional[str] = None,
        validate: Optional[callable] = None,
        **kwargs
    ) -> Optional[str]:
        """
        Ask the user to input text.
        
        :param message: The message to display.
        :param default: The default value.
        :param validate: A function to validate the user's response.
        :param kwargs: Keyword arguments to pass to the prompt.
        
        :return: The user's response.
        """

        return cls._convert_to_inquirer(
            'text',
            message = message,
            default = default,
            validate = validate,
            **kwargs
        )
    
    @classmethod
    def integer(
        cls,
        message: str,
        default: Optional[int] = None,
        validate: Optional[callable] = None,
        **kwargs
    ) -> Optional[int]:
        """
        Ask the user to input an integer.
        
        :param message: The message to display.
        :param default: The default value.
        :param validate: A function to validate the user's response.
        :param kwargs: Keyword arguments to pass to the prompt.
        
        :return: The user's response.
        """

        response = cls._convert_to_inquirer(
            'text',
            message = message,
            default = str(default) if default else None,
            validate = lambda x: (
                (x == '' or x.isdigit())
                and (validate(
                    int(x) if x.isdigit() else x
                ) if validate else True)
            ),
            **kwargs
        )

        return int(response) if response else None
    
    @classmethod
    def float(
        cls,
        message: str,
        default: Optional[float] = None,
        validate: Optional[callable] = None,
        **kwargs
    ) -> Optional[float]:
        """
        Ask the user to input a float.
        
        :param message: The message to display.
        :param default: The default value.
        :param validate: A function to validate the user's response.
        :param kwargs: Keyword arguments to pass to the prompt.
        
        :return: The user's response.
        """

        response = cls._convert_to_inquirer(
            'text',
            message = message,
            default = str(default) if default else None,
            validate = lambda x: (
                (x == '' or x.replace('.', '', 1).isdigit())
                and (validate(
                    float(x) if x.replace('.', '', 1).isdigit() else x
                ) if validate else True)
            ),
            **kwargs
        )

        return float(response) if response else None
    
    @classmethod
    def date(
        cls,
        message: str,
        default: Optional[datetime] = None,
        validate: Optional[callable] = None,
        **kwargs
    ) -> Optional[datetime]:
        """
        Ask the user to input a date.
        
        :param message: The message to display.
        :param default: The default value.
        :param validate: A function to validate the user's response.
        :param kwargs: Keyword arguments to pass to the prompt.
        
        :return: The user's response.
        """

        response = cls._convert_to_inquirer(
            'text',
            message = message,
            default = default.strftime('%Y-%m-%d') if default else None,
            validate = lambda x: (
                (x == '' or validate_date(x))
                and (
                    validate(
                        datetime.strptime(x, '%Y-%m-%d') if x else x
                    ) if validate else True
                )
            ),
            **kwargs
        )

        return datetime.strptime(response, '%Y-%m-%d') if response else None

    @classmethod
    def datetime(
        cls,
        message: str,
        default: Optional[datetime] = None,
        validate: Optional[callable] = None,
        **kwargs
    ) -> Optional[datetime]:
        """
        Ask the user to input a datetime.
        
        :param message: The message to display.
        :param default: The default value.
        :param validate: A function to validate the user's response.
        :param kwargs: Keyword arguments to pass to the prompt.
        
        :return: The user's response.
        """

        response = cls._convert_to_inquirer(
            'text',
            message = message,
            default = (
                default.strftime('%Y-%m-%d %H:%M:%S')
                if default else None
            ),
            validate = lambda x: (
                (x == '' or validate_datetime(x))
                and (
                    validate(
                        datetime.strptime(x, '%Y-%m-%d %H:%M:%S') if x else x
                    ) if validate else True
                )
            ),
            **kwargs
        )

        return (
            datetime.strptime(response, '%Y-%m-%d %H:%M:%S')
            if response else None
        )

    @classmethod
    def csv(
        cls,
        message: str,
        default: Optional[list] = None,
        validate: Optional[callable] = None,
        **kwargs
    ) -> list:
        """
        Ask the user to input a comma-separated list of values.
        
        :param message: The message to display.
        :param default: The default value.
        :param validate: A function to validate the user's response.
        :param kwargs: Keyword arguments to pass to the prompt.
        
        :return: The user's response.
        """

        if default:
            default = ','.join(default)

        response = cls._convert_to_inquirer(
            'text',
            message = message,
            default = default,
            validate = (lambda x: (
                validate(
                    [x.strip() for x in x.split(',')] if x else x
                )
            )) if validate else None,
            **kwargs
        )

        response = response.split(',') if response else []
        response = [value.strip() for value in response]

        return response
    
    @classmethod
    def json(
        cls,
        message: str,
        default: Optional[dict] = None,
        validate: Optional[callable] = None,
        **kwargs
    ) -> dict:
        """
        Ask the user to input a JSON object.
        
        :param message: The message to display.
        :param default: The default value.
        :param validate: A function to validate the user's response.
        :param kwargs: Keyword arguments to pass to the prompt.
        
        :return: The user's response.
        """

        if default:
            default = json.dumps(default)

        response = cls._convert_to_inquirer(
            'text',
            message = message,
            default = default,
            validate = (lambda x: (
                (x == '' or validate_json(x))
                and validate(
                    json.loads(x) if x else x
                ) if validate else True
            )) if validate else None,
            **kwargs
        )

        return json.loads(response) if response else {}

    @classmethod
    def editor(
        cls,
        message: str,
        default: Optional[str] = None,
        validate: Optional[callable] = None,
        **kwargs
    ) -> str:
        """
        Ask the user to input text using an editor.
        
        :param message: The message to display.
        :param default: The default value.
        :param validate: A function to validate the user's response.
        :param kwargs: Keyword arguments to pass to the prompt.
        
        :return: The user's response.
        """
        
        return cls._convert_to_inquirer(
            'editor',
            message = message,
            default = default,
            validate = validate,
            **kwargs
        )

    @classmethod
    def path(
        cls,
        message: str,
        default: Optional[Union[str, os.PathLike]] = None,
        validate: Optional[callable] = None,
        path_type: Literal['file', 'directory', 'any'] = 'any',
        exists: Optional[bool] = None,
        normalize_to_absolute_path: bool = False,
        **kwargs
    ) -> Path:
        """
        Ask the user to input a path.
        
        :param message: The message to display.
        :param default: The default value.
        :param validate: A function to validate the user's response.
        :param path_type: The type of path to accept.
        :param exists: Whether the path must exist or not.
        :param normalize_to_absolute_path: Whether to normalize the path to an
            absolute path or not.
        :param kwargs: Keyword arguments to pass to the prompt.
        
        :return: The user's response.
        """

        if default:
            default = str(Path(default).resolve())

        response = cls._convert_to_inquirer(
            'path',
            message = message,
            default = default,
            validate = (lambda x: validate(Path(x))) if validate else None,
            path_type = path_type,
            exists = exists,
            normalize_to_absolute_path = normalize_to_absolute_path,
            **kwargs
        )

        return Path(response) if response else None

    @classmethod
    def password(
        cls,
        message: str,
        default: Optional[str] = None,
        validate: Optional[callable] = None,
        **kwargs
    ) -> str:
        """
        Ask the user to input a password.

        :param message: The message to display.
        :param default: The default value.
        :param validate: A function to validate the user's response.
        :param kwargs: Keyword arguments to pass to the prompt.

        :return: The user's response.
        """

        return cls._convert_to_inquirer(
            'password',
            message = message,
            default = default,
            validate = validate,
            **kwargs
        )

    @classmethod
    def checkbox(
        cls,
        message: str,
        choices: Union[List[str], List[Tuple[str, Any]]],
        default: Optional[Union[List[str], List[Any]]] = None,
        validate: Optional[callable] = None,
        **kwargs
    ) -> List[Any]:
        """
        Ask the user to select one or more options from a list.
        
        :param message: The message to display.
        :param choices: The list of choices.
        :param default: The default value.
        :param validate: A function to validate the user's response.
        :param kwargs: Keyword arguments to pass to the prompt.
        
        :return: The user's response.
        """

        return cls._convert_to_inquirer(
            'checkbox',
            message = message,
            choices = choices,
            default = default,
            validate = validate,
            **kwargs
        )

    @classmethod
    def list(
        cls,
        message: str,
        choices: Union[List[str], List[Tuple[str, Any]]],
        validate: Optional[callable] = None,
        **kwargs
    ) -> Any:
        """
        Ask the user to select one option from a list.

        :param message: The message to display.
        :param choices: The list of choices.
        :param validate: A function to validate the user's response.
        :param kwargs: Keyword arguments to pass to the prompt.

        :return: The user's response.
        """
        
        return cls._convert_to_inquirer(
            'list',
            message = message,
            choices = choices,
            validate = validate,
            **kwargs
        )

    @staticmethod
    def _convert_to_inquirer(
        method: str,
        message: str,
        choices: Optional[Union[List[str], List[Tuple[str, Any]]]] = None,
        default: Optional[str] = None,
        validate: Optional[callable] = None,
        **kwargs
    ):
        """
        Convert the method name to the corresponding inquirer method.

        :param method: The method name.
        :param message: The message to display.
        :param choices: The list of choices.
        :param default: The default value.
        :param validate: A function to validate the user's response.
        :param kwargs: The keyword arguments.

        :return: The result of the inquirer method.

        :raises AttributeError: If the method name is not valid.
        """

        pause_event.set()
        sleep(1/2)

        arguments = {
            'message': message,
            'choices': choices if method in ['checkbox', 'list'] else None,
            'default': default,
            'validate': (lambda _, x: validate(x)) if validate else None,
            **kwargs
        }

        cleaned_arguments = {
            key: value for key, value in arguments.items()
            if value is not None
        }

        questions = [
            getattr(inquirer, method.capitalize())(
                'answer',
                **cleaned_arguments
            )
        ]

        try:
            result = inquirer.prompt(
                questions,
                theme = PromptTheme(),
                raise_keyboard_interrupt = True
            )
        
        except KeyboardInterrupt:
            if not ask_for_interrupt():
                result = Prompt._convert_to_inquirer(
                    method,
                    **arguments
                )

        pause_event.clear()
        sleep(1/2)

        return result['answer'] if result else None