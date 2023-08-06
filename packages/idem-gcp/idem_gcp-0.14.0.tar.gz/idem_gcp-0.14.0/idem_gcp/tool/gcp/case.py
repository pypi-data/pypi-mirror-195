import re


def camel(hub, string: str, dromedary: bool = True) -> str:
    """
    Change a snake-cased string to a camel-cased string
    """
    if "_" not in string and (dromedary or string[0].isupper()):
        # Already cameled
        return string
    else:
        # Replace underscores with spaces then call str()'s title() method, then get rid of spaces
        result = string.replace("_", " ").title().replace(" ", "")
        if dromedary:
            return result[0].swapcase() + result[1:]
        return result


def is_camel_case(hub, value: str) -> bool:
    return hub.tool.gcp.case.camel(value) == value


# TODO: Write a test to validate corner cases like abcXTZ
def snake(hub, string: str) -> str:
    """
    Change a camel-cased string to a snake-cased string
    """

    # Separate each camel-cased word into underscore delimited words
    string = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    string = re.sub("([a-z0-9])([A-Z])", r"\1_\2", string)
    # Replace special characters with underscores except for [] and .
    string = re.sub(r"[^\w\[\]\.]", "_", string)
    # make sure everything is lower-cased
    string = string.lower()
    string = string.replace("__", "_")

    return string


def sanitize_key(hub, key: str) -> str:
    return hub.tool.format.keyword.unclash(hub.tool.gcp.case.snake(key))


def is_snake_case(hub, value: str) -> bool:
    return hub.tool.gcp.case.snake(value) == value


def is_unclashed(hub, value: str) -> bool:
    return hub.tool.format.keyword.unclash(value) == value
