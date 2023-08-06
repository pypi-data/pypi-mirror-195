import functools
import logging
import os
import time

logger = logging.getLogger(__name__)


def log_on_exception(_func=None, *, acceptable_exceptions=Exception):
    """
    ---------------------------------------------------------------------------------------------
    Decorator to log exception but not fail (default: Exception)
    ---------------------------------------------------------------------------------------------

    NOTE: Use with caution! Specified Exceptions will be eaten and None will be returned, might
          lead to unexpected situations on the 'decorated function' caller.
    Usage:

        @log_on_exception
        def get_data(*args, **kwargs):
            client.get_required_data(arg1)

    Examples:

        1. Log and return if Exception encountered (Default):
        @log_on_exception

        2. Log and return if IndexError encountered (Default):
        @log_on_exception(acceptable_exceptions=IndexError)

    """

    def decorator(_func):
        @functools.wraps(_func)
        def wrapper(*args, **kwargs):
            try:
                return _func(*args, **kwargs)
            except acceptable_exceptions:
                logger.exception(f'Exception occurred while running {_func.__name__}. Returning None to caller!')
            return None

        return wrapper

    return decorator if _func is None else decorator(_func)


def retry_on_exception(_func=None, *, num_retries=3, retry_exceptions=Exception, exception_handler=None, delay=0):
    """
    ---------------------------------------------------------------------------------------------
    Retry the function num_retries (default: 3) on encountering an exception (default: Exception)
    ---------------------------------------------------------------------------------------------

    Usage:

        @retry_on_exception
        def get_data(*args, **kwargs):
            client.get_required_data(arg1)

    Examples:

        1. Retry 3 times if Exception encountered (Default):
        @retry_on_exception

        2. Retry 1 time if IndexError encountered:
        @retry_on_exception(retry_exceptions=IndexError, num_retries=1)

        3. Retry 2 times if IndexError or ValueError encountered:
        @retry_on_exception(retry_exceptions=(IndexError, ValueError), num_retries=2)

        4. Retry 3 times if IndexError or ValueError with Linear delay of 5 seconds:
        @retry_on_exception(retry_exceptions=(IndexError, ValueError), num_retries=3, delay=5)
        First retry will be after 5 secs, second after (5+)10 secs and third after (5+10+)15 secs

    """

    def decorator_retry(_func):
        @functools.wraps(_func)
        def wrapper_retry(*args, **kwargs):
            for i in range(num_retries):
                try:
                    return _func(*args, **kwargs)
                except retry_exceptions:
                    logger.exception(
                        f'Exception occurred while running {_func.__name__} ' f'on attempt {i+1} out of {num_retries}.'
                    )
                    if type(delay) == int and delay > 0:
                        if exception_handler:
                            logger.warning(f'Executing {exception_handler.__name__}.')
                            exception_handler()
                        linear_delay = (i + 1) * delay
                        time.sleep(linear_delay)
                        logger.info(f'Retrying {_func.__name__} {i+1} time after {linear_delay} seconds.')
            return _func(*args, **kwargs)

        return wrapper_retry

    return decorator_retry if _func is None else decorator_retry(_func)


def function_not_implemented(error_message_prefix=None, error_message_suffix=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            error_message = f'{func.__name__} not implemented!'

            if error_message_prefix and type(error_message_prefix) is str:
                if error_message_prefix[-1] != ' ':
                    error_message = error_message_prefix + ' ' + error_message
                else:
                    error_message = error_message_prefix + error_message

            if error_message_suffix and type(error_message_suffix) is str:
                error_message += ' ' + error_message_suffix

            raise NotImplementedError(error_message)

        return wrapper

    return decorator


def are_we_in_test_mode():
    settings_module_string = os.environ.get("DJANGO_SETTINGS_MODULE", "local").split(".")[-1]
    return 'local' in settings_module_string or 'test' in settings_module_string


def skip_in_test_mode(f):
    def internal(*args, **kwargs):
        if not are_we_in_test_mode():
            return f(*args, **kwargs)
        return None

    return internal
