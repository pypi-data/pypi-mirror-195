import os


def datadog_enabled():
    return os.environ.get('DD_TRACE_ENABLED')
