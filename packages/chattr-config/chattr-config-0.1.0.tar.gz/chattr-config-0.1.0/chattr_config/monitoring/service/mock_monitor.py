from chattr_config.monitoring.service.monitor import Monitor
from typing import List, Union
import logging
import time

logger = logging.getLogger('django')


class MockMonitor(Monitor):

    name = 'MockMonitor'

    def __init__(self):
        super().__init__()

    def increment_metric(self, metric: str, tags: List[str]) -> None:
        pass

    def timer(self, metric: str, tags: List[str]) -> object:
        class TimedContextManagerDecorator(object):
            def __enter__(self):
                self.start = time.time()

            def __exit__(self, type, value, traceback):
                end = time.time()
                logger.info(f'Metric: {metric} with tags: {tags} took {end-self.start} secs')

        return TimedContextManagerDecorator()

    def send_metric(self, metric: str, value: Union[int, float], tags: List[str]) -> None:
        pass
