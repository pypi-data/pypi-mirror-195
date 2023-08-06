from typing import List
from .trigger import Trigger
from .job import JobConfig
import time
from datetime import datetime


class Scheduler:
    def __init__(self) -> None:
        self.job_configs = []

    def add_job_config(self, name: str, execution_cmd_args: List[str], trigger: Trigger):
        self.job_configs.append(
            JobConfig(name, execution_cmd_args, trigger)
        )

    def start(self):
        while True:
            utc_now = datetime.utcnow()
            min_trigger = min(
                map(lambda x: x.next_trigger_datetime, self.job_configs))
            for job_conf in self.job_configs:
                job_conf.trigger_if_necessary(utc_now)
            print(f'loop {min_trigger-utc_now}')
            time.sleep(1)
