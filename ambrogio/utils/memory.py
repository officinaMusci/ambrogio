from typing import Union, Optional


def format_bytes(bytes: Union[int, float]) -> Optional[str]:
    """
    Format bytes to KB, MB, GB, TB

    :param bytes: The number of bytes to format.

    :return: The formatted bytes.
    """

    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return "%3.1f %s" % (bytes, x)
        bytes /= 1024.0