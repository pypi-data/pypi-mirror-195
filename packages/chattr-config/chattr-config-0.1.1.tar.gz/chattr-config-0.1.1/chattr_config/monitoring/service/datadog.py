from chattr_config.monitoring.service.monitor import Monitor
from datadog import statsd
from typing import Union, List
from chattr_config.decorators.decorators import log_on_exception


class DatadogMonitor(Monitor):

    name = 'Datadog'

    def __init__(self):
        super().__init__()
        self.statsd = statsd

    @log_on_exception
    def increment_metric(self, metric: str, tags: List[str]) -> None:
        self.statsd.increment(metric, tags=tags)

    @log_on_exception
    def timer(self, metric: str, tags: List[str]) -> object:
        return statsd.timed(metric, tags=tags)

    @log_on_exception
    def send_metric(self, metric: str, value: Union[int, float], tags: List[str]) -> None:
        statsd.histogram(metric, value, tags=tags)
