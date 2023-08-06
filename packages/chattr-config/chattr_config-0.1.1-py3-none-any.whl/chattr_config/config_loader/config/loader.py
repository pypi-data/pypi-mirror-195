# This has nothing to do with custom settings per brand.  It doesn't have that much granularity.
# We can have something that the server can turn on and off for feature flags here.

# Load yaml file based upon 'env' variable.

# Direction is to pull from SSM to start as well.

# Pull in environment variables.

# Order importance:
#   - ENV variable; these should be extremely rare
#   - SSM variable; these are _only_ for secrets and things that could be more easily configurable.
#   - yaml config file that pulls in all variables that pivots it.

import os
import logging
from typing import Any, Dict, Iterable, List

from chattr_config.config_loader.borg import Borg
from chattr_config.config_loader.ssm_loader import SSMLoader
from chattr_config.config_loader.yaml_loader import YamlLoader

from .definitions import ConfigDefinitions


_logger = logging.getLogger(__name__)


class ConfigImpl(Borg):
    def __init__(self) -> None:
        """Constructor for configuration."""
        super().__init__()
        self.lookup_table: Dict[str, Any] = {}
        self.loaded = False

    def init(self, var_file: str, value_files: List[str], ssm_folder: str = None, ssm_client=None):
        """Loads up the files into yaml and validate that all values
            are correctly filled.

        Args:
            var_file (str): Variable declaration file that then will iterate
                and find the needed from configuration on load
            value_files (List[str]): Files that contain value that can be shared across yaml files
            ssm_folder (str): base path for secrets storage.
            ssm_client (botocore.client.SSM): boto3 ssm client object
        Returns:
            Errors on loading the yaml files.
        """
        validator = ConfigDefinitions(var_file)
        validator.load()
        config_data: Dict[str, Any] = {}
        # The last one in the list has the highest priority
        for file in value_files:
            file_data = YamlLoader.load_file(file)
            config_data.update(file_data)

        # SSM is highest priority except for environment variables
        if ssm_folder and os.environ.get('SSM_LOADER_DISABLED', '').lower() not in ['true', '1']:
            # Merge SSM value into the necessary dictionary after load.
            ssm_data = SSMLoader(prefix=ssm_folder, ssm_client=ssm_client)
            config_data = {**config_data, **ssm_data}

        config_data.update(self._load_environ_values(validator.keys()))

        # Ask ConfigDefinitions to validate and normalize the resultant dictionary.
        self.lookup_table, errors = validator.transform(config_data)
        if errors:
            raise Exception("Unable to load configurations.  Check logs for problems with config")

        self.loaded = True

    def _load_environ_values(self, keys: Iterable[str]) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        for key in keys:
            result = os.environ.get(key, None)
            if result is not None:
                data[key] = result
        return data

    '''
    We cast all values after we load the definitions file. Prefer using `get`
    over these individual methods. If the type is wrong, fix the definitions file.
    '''

    def int_value(self, name: str, default: int = -1) -> int:
        _logger.warning('`int_value` will be removed in a future release. Use `get` for retrieving config values.')
        return self._get_value(name, default, int, "int")

    def str_value(self, name: str, default: str = "") -> str:
        _logger.warning('`str_value` will be removed in a future release. Use `get` for retrieving config values.')
        return self._get_value(name, default, str, "str")

    def bool_value(self, name: str, default: bool = False) -> bool:
        _logger.warning('`bool_value` will be removed in a future release. Use `get` for retrieving config values.')
        return self._get_value(name, default, bool, "bool")

    def float_value(self, name: str, default: float = 0.0) -> float:
        _logger.warning('`float_value` will be removed in a future release. Use `get` for retrieving config values.')
        return self._get_value(name, default, float, "float")

    def _get_value(self, name: str, default: Any, field_type, field_type_name: str = "") -> Any:
        if not self.loaded:
            raise Exception("Not initialized")
        result = self.lookup_table.get(name)
        if result is None:
            result = default
        elif not isinstance(result, field_type):
            raise ValueError(f"{name} is not of type {field_type_name}")
        return result

    def get(self, name: str, default: Any = None) -> Any:
        if not self.loaded:
            raise Exception("Not initialized")
        result = self.lookup_table.get(name)
        if result is None:
            result = default
        return result


ConfigData = ConfigImpl()
