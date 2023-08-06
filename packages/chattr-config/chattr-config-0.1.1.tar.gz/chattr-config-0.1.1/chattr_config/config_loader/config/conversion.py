from typing import Any

# bool() returns true on any defined value
# strtobool() can't handle a bool being passed in
# anything else is just a false.
def evalbool(value: Any) -> bool:
    return_value: bool = False
    if type(value) is bool:
        return_value = value

    if type(value) is str:
        if value.lower() in ('y', 'yes', 't', 'true', 'on', '1'):
            return_value = True

    if type(value) is int:
        if value == 1:
            return_value = True

    return return_value
