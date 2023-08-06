import os

import pendulum

from chattr_config.monitoring.context import Context
from chattr_config.utils.system_utils import get_machine_info

from .base_json_log_formatter import JSONFormatter


class ChattrJSONFormatter(JSONFormatter):
    """
    Custom class to override the default behaviour of the JSONFormatter
    """

    def format(self, record):
        """
        the default behaviour of JSONFormatter is to cast everything into a string
        we avoid calling getMessage and leave the object as it is, this way our json messages can have nested dicts
        """
        message = record.getMessage()
        extra = self.extra_from_record(record)
        json_record = self.json_record(message, extra, record)
        mutated_record = self.mutate_json_record(json_record)
        # Backwards compatibility: Functions that overwrite this but don't
        # return a new value will return None because they modified the
        # argument passed in.
        if mutated_record is None:
            mutated_record = json_record
        mutated_record.update({'machine_info': get_machine_info()})
        mutated_record.update({'context': Context.acquire().to_dict()})
        return self.to_json(mutated_record)

    def json_record(self, message, extra, record):
        extra['level'] = record.levelname
        extra['module'] = record.name
        extra['time'] = pendulum.now()
        extra['message'] = message
        extra['func_name'] = f"{record.module}.{record.funcName}:{record.lineno}"

        if record.exc_info:
            extra['exec_info'] = self.formatException(record.exc_info)
        return extra

    def to_json(self, record):
        """Converts record dict to a JSON string.

        It makes best effort to serialize a record (represents an object as a string)
        instead of raising TypeError if json library supports default argument.
        Note, ujson doesn't support it.
        """
        return self.json_lib.dumps(record, default=_json_object_encoder)


def _json_object_encoder(obj):
    try:
        return obj.to_json()
    except AttributeError:
        return str(obj)
