import time


class Timer:
    """
    Hold and format elapsed time.
    """

    beginning: float = 0
    end: float = 0

    def __init__(self, start: bool = True) -> None:
        if start:
            self.start()

    @property
    def elapsed_time(self) -> str:
        """
        Return the elapsed time in the format HH:MM:SS.

        :return: The formatted elapsed time.
        """

        return self.format_elapsed_time(
            self.beginning,
            self.end or time.time()
        )

    def start(self) -> None:
        """
        Start the timer.
        """

        self.beginning = time.time()

    def stop(self) -> None:
        """
        Stop the timer.
        """

        self.end = time.time()

    @staticmethod
    def format_elapsed_time(start: float, end: float) -> str:
        """
        Format elapsed time.
        
        :param start: The start time.
        :param end: The end time.

        :return: The formatted elapsed time.
        """
        
        hours, rem = divmod(end - start, 3600)
        minutes, seconds = divmod(rem, 60)

        elapsed_time = "{:0>2}:{:0>2}:{:05.3f}".format(
            int(hours),
            int(minutes),
            seconds
        )

        return elapsed_time