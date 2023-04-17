from threading import Event
from time import sleep


# Event used to interrupt threads when exceptions are raised
exit_event = Event()

# Event used to pause threads
pause_event = Event()


def wait_resume():
    """
    Wait for the pause event to be cleared.
    """

    while pause_event.is_set():
        sleep(1/4)


def check_events() -> bool:
    """
    Check if the exit and pause events are not set.
    """

    return not exit_event.is_set() and not pause_event.is_set()