"""Define Jobs to be executed
"""

from typing import List
from threading import Thread
import subprocess
import io
import time
from datetime import datetime

from .trigger import Trigger


class JobExecution(Thread):
    """Class that executes a job for a single time
    """

    def __init__(self, execution_cmd_args: List[str]) -> None:
        super().__init__(target=self._trigger_and_log)
        self.execution_cmd_args = execution_cmd_args
        self.lines = []
        self.error_message = None
        self.return_code = None
        self.duration = None

    def _execute(self) -> None:
        process = subprocess.Popen(  # pylint: disable=consider-using-with
            args=self.execution_cmd_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,

        )

        for line in io.TextIOWrapper(process.stdout, encoding="utf-8", errors='ignore'):
            yield line

        self.return_code = process.wait()
        self.error_message = process.stderr.read().decode()

    def _trigger_and_log(self) -> None:
        start_time = time.time()
        for line in self._execute():
            self.lines.append(line)
        end_time = time.time()

        self.duration = end_time-start_time


class JobConfig:
    """Class that configures a job execution and triggers them if necessary
    """

    def __init__(self, name: str, execution_cmd_args: List[str], trigger: Trigger) -> None:
        self.name = name
        self.execution_cmd_args = execution_cmd_args
        self.trigger = trigger

        self.next_trigger_datetime = trigger.calculate_next_trigger()
        self.executions = []
        self.current_execution = None

    def trigger_if_necessary(self, current_datetime: datetime):
        """Handles the triggering logic of the job. Sets a new trigger time if necessary.

        Args:
            current_datetime (datetime): The current datetime provided from outside
        """
        if self.current_execution and self.current_execution.is_alive():
            print(f'{self.name} in running')
            return

        if self.current_execution and not self.current_execution.is_alive():
            self.current_execution = None
            self.next_trigger_datetime = self.trigger.calculate_next_trigger()
            print(f'{self.name} finished')
            return

        if current_datetime > self.next_trigger_datetime and not self.current_execution:
            self.current_execution = JobExecution(self.execution_cmd_args)
            self.current_execution.start()
            self.executions.append(self.current_execution)
            print(f'triggering {self.name}')
            return
