import time


class Timer:
    """
    Hold and format elapsed time
    """

    beginning: float|None = None
    end: float|None = None

    def __init__(self, start: float = True) -> None:
        if start:
          self.start()

    def start(self) -> None:
        self.beginning = time.time()

    def stop(self) -> None:
        self.end = time.time()

    def get_elapsed_time(self) -> str:
        return self.format_elapsed_time(
            self.beginning,
            self.end or time.time()
        )

    @staticmethod
    def format_elapsed_time(start: float, end: float) -> str:
        hours, rem = divmod(end - start, 3600)
        minutes, seconds = divmod(rem, 60)

        elapsed_time = "{:0>2}:{:0>2}:{:05.2f}".format(
            int(hours),
            int(minutes),
            seconds
        )

        return elapsed_time