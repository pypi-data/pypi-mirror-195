from abc import ABC, abstractmethod
from typing import Union, List


class Monitor(ABC):
    name = 'AbstractMonitor'
    acceptable_tags = ['producer', 'consumer', 'topic', 'environment', 'brand_id', 'status', 'task', 'queue']

    def get_tags(self, **tags_dict: str) -> List[str]:
        return [f'{tag}:{tags_dict.get(tag)}' for tag in self.acceptable_tags]

    @abstractmethod
    def increment_metric(self, metric: str, tags: List[str]) -> None:
        pass

    @abstractmethod
    def timer(self, metric: str, tags: List[str]) -> object:
        pass

    @abstractmethod
    def send_metric(self, metric: str, value: Union[int, float], tags: List[str]) -> None:
        pass
