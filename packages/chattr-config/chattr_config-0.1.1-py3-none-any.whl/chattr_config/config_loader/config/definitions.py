import json

import dataclasses
import logging
from typing import Any, Callable, Dict, List, Set, Tuple, Union, Optional

from chattr_config.config_loader.config.conversion import evalbool
from chattr_config.config_loader.yaml_loader import YamlLoader


@dataclasses.dataclass(frozen=True)
class DefinitionsData:
    name: str
    value: Union[int, float, bool, str]
    type_name: str
    cast_method: Callable
    secret: bool = False
    required: bool = False


cast_methods = {
    "bool": evalbool,
    "float": float,
    "int": int,
    "string": str,
    'json': json.loads,
}


class ConfigDefinitions:
    def __init__(self, var_file: str) -> None:
        """Constructor for definitions file.

        Args:
            var_file (str): Variable declaration file that then will iterate
                and find the needed from configuration on load
        """
        self.var_file = var_file
        self.definition: Dict[str, DefinitionsData] = {}

    def load(self):
        """Loads up the files into yaml and validate that all values
            are correctly filled.

        Returns:
            Errors on loading the yaml files.
        """
        data = YamlLoader.load_file(self.var_file)
        self.definitions = self._parse_definitions(data)
        self.required_items = {key for key, value in self.definitions.items() if value.required is True}
        self.defaults = {key: value for key, value in self.definition.items() if value.value is not None}

    def transform(self, input_data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Exception]]:
        """Iterates through the dictionary of key:value pairs
            and casts to the appropriate type.
        Args:
            input_data (Dict[str, Any]): Input data with each key being an entry in the definitions
                that defines what it uses.

        Returns:
            List[ValueError]: [description]
        """
        errors: List[Exception] = []
        result: Dict[str, Any] = {}
        for key, definition in self.definitions.items():
            value = input_data.get(key, definition.value)
            try:
                result[key] = cast_methods[definition.type_name](value) if value is not None else None
            except ValueError as e:
                logging.error(f"Cannot cast {key}:{value} to defined type {definition.type_name}")
                errors.append(e)

        # add input the dictionary any defaults that do not exist in the result
        unfilled_keys = self.defaults.keys() - result.keys()
        for key in unfilled_keys:
            result[key] = self.defaults[key]

        # check if all required items are accounted for
        has_default_values = {k: v for k, v in result.items() if v is not None}
        unknown_keys: Set[str] = self.required_items - set(list(has_default_values.keys()))
        if unknown_keys:
            logging.error(f"Unaccounted for required keys {unknown_keys}")
            raise ValueError(f"Missing values for {sorted(unknown_keys)}")

        return result, errors

    def keys(self) -> Set[str]:
        return set(self.definitions.keys())

    def _parse_definitions(self, config_data: Dict[str, Any]) -> Dict[str, DefinitionsData]:
        output: Dict[str, DefinitionsData] = {}
        errors: List[Exception] = []
        for key, value in config_data.items():
            try:
                data = value.get("value")
                type_data = value.pop("type")
                value["type_name"] = type_data
                cast_method = cast_methods[type_data]
                if data is None:
                    value["value"] = None
                value["cast_method"] = cast_method
                output[key] = DefinitionsData(name=key, **value)
            except Exception as e:
                logging.error(f"Errors found parsing: {key}:{value}")
                print(e)
                errors.append(e)
        if errors:
            logging.error("Check logs for failed definitions loader")
            raise Exception("Unable to load definitions file")

        return output
