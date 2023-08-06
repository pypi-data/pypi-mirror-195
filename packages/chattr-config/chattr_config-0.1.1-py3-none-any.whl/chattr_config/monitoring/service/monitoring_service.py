import logging
import os
from chattr_config.monitoring.service.datadog import DatadogMonitor
from chattr_config.monitoring.service.monitor import Monitor
from chattr_config.monitoring.service.mock_monitor import MockMonitor
from singleton_decorator import singleton
from typing import Union, List


@singleton
class MonitoringService(object):
    def __init__(self, monitor=None, logger=logging.getLogger('django')):
        self.monitor = monitor or MockMonitor()
        self.logger = logger

    def get_monitor_name(self):
        return self.monitor.name

    def get_tags(self, **tags_dict) -> List[str]:
        return self.monitor.get_tags(**tags_dict)

    def increment_metric(self, metric: str, tags: List[str]) -> None:
        self.monitor.increment_metric(metric, tags)

    def timer(self, metric: str, tags: List[str]):
        return self.monitor.timer(metric, tags)

    def send_metric(self, metric: str, value: Union[int, float], tags: List[str]):
        return self.monitor.send_metric(metric, value, tags)
