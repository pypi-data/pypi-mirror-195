import logging
import os
import random
import time
from typing import Any

from boto3.session import Session

_logger = logging.getLogger(__name__)

MAX_FAILED_ATTEMPTS = 3


class SSMLoader:
    """
    Provide a dictionary-like interface to access AWS SSM Parameter Store
    """

    def __init__(self, prefix=None, ssm_client=None):
        self._prefix = (prefix or '').rstrip('/') + '/'
        self._client = ssm_client or self._make_client()
        self._keys = {}
        self._sub_stores = {}

    def _make_client(self):
        aws_region = os.environ.get('AWS_DEFAULT_REGION') or 'us-west-2'
        return Session(region_name=aws_region).client('ssm')

    def _get_all_dataparams(self, base_path: str):
        """root of all parameters that is to be pulled out
            (dev/stg/prf/prd)/(config|microservicename)/settings

        Args:
            base_path (str): base of services code.
        """
        data = []
        query = {'Path': base_path, 'Recursive': True, 'WithDecryption': True}
        done = False
        while not done:
            result = self._client.get_parameters_by_path(**query)
            meta = result['ResponseMetadata']
            if meta['HTTPStatusCode'] == 429:
                self._back_off(meta['RetryAttempts'])
            parameters = [(item['Name'], item['Value']) for item in result['Parameters']]
            data.extend(parameters)
            query['NextToken'] = next_token = result.get('NextToken')
            if len(parameters) < 1 or not next_token:
                done = True

        start_at = len(base_path)
        return {item[0][start_at:].upper(): item[1] for item in data}

    def _back_off(self, failed_attempts: int):
        if failed_attempts > MAX_FAILED_ATTEMPTS:
            raise Exception(f'SSM Load Failed with too many failed attempts {failed_attempts}')

        jitter = random.randint(0, 2000)
        sleep_time = ((2 << failed_attempts) * 1000 + jitter) / 1000
        _logger.warning(f'Backing off {sleep_time} with failed_attempts {failed_attempts}')
        time.sleep(sleep_time)

    def get(self, name: str, **kwargs) -> Any:
        if not self._keys:
            self.refresh()

        if name not in self._keys:
            if 'default' in kwargs:
                return kwargs['default']
            raise KeyError(name)
        else:
            return self._get_value(name)

    def refresh(self):
        self._keys = {}
        self._keys = self._get_all_dataparams(self._prefix)

    def keys(self) -> list:
        if not self._keys:
            self.refresh()
        return self._keys.keys()

    def _get_value(self, name) -> Any:
        return self._keys[name]

    def __contains__(self, name: str) -> bool:
        try:
            self.get(name)
        except (AttributeError, KeyError):
            return False
        else:
            return True

    def __getitem__(self, name: str) -> Any:
        return self.get(name)

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __delitem__(self, name):
        raise NotImplementedError

    def __repr__(self) -> str:
        return f'ParameterStore[{self._prefix}]'
