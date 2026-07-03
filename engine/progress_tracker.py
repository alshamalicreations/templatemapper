"""
progress_tracker.py

Tracks migration progress.
"""

from time import perf_counter


class ProgressTracker:

    def __init__(
        self,
        total_operations,
        callback=None,
    ):

        self.total = max(total_operations, 1)

        self.current = 0

        self.callback = callback

        self.last_percentage = -1

        self.start_time = perf_counter()

    def advance(self, amount=1):

        self.current += amount

        if self.current > self.total:

            self.current = self.total

        percentage = int(
            (self.current / self.total) * 100
        )

        if percentage != self.last_percentage:

            self.last_percentage = percentage

            if self.callback:

                self.callback(percentage)

    @property
    def percentage(self):

        return int(
            (self.current / self.total) * 100
        )

    @property
    def current_operations(self):

        return self.current

    @property
    def total_operations(self):

        return self.total

    @property
    def remaining_operations(self):

        return self.total - self.current

    @property
    def elapsed_time(self):

        return perf_counter() - self.start_time

    @property
    def operations_per_second(self):

        if self.elapsed_time <= 0:

            return 0

        return self.current / self.elapsed_time

    @property
    def eta_seconds(self):

        speed = self.operations_per_second

        if speed <= 0:

            return 0

        return self.remaining_operations / speed