"""Classes for triggering jobs on a schedule
"""

from datetime import time, datetime, timedelta


class Trigger:
    """Abstract Trigger Class
    """

    def calculate_next_trigger(self) -> datetime:
        """Calculates the next time the trigger fill fire

        Returns:
            datetime: _description_
        """
        raise NotImplementedError


class PeriodicTrigger(Trigger):
    def __init__(self, time_delta: timedelta) -> None:
        super().__init__()
        self.time_delta = time_delta

    def calculate_next_trigger(self):
        return datetime.utcnow() + self.time_delta


class TimeTrigger(Trigger):
    def __init__(self, trigger_time: time) -> None:
        super().__init__()
        self.trigger_time = trigger_time

    def calculate_next_trigger(self):
        now = datetime.utcnow().date()
        trigger_datetime = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=self.trigger_time.hour,
            minute=self.trigger_time.minute,
            second=self.trigger_time.second,
            microsecond=self.trigger_time.microsecond
        )

        if now < trigger_datetime:
            return trigger_datetime
        else:
            return trigger_datetime + timedelta(days=1)
