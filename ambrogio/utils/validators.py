from datetime import datetime
import json



def validate_date(date: str) -> bool:
    """
    Validate a date.

    :param date: The date to validate.

    :return: Whether the date is valid.
    """

    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return False
    else:
        return True
    

def validate_datetime(datetime: str) -> bool:
    """
    Validate a datetime.

    :param datetime: The datetime to validate.

    :return: Whether the datetime is valid.
    """

    try:
        datetime.strptime(datetime, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return False
    else:
        return True
    

def validate_json(json: str) -> bool:
    """
    Validate a JSON string.

    :param json: The JSON string to validate.

    :return: Whether the JSON string is valid.
    """

    try:
        json.loads(json)
    except ValueError:
        return False
    else:
        return True