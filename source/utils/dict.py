from typing import Callable, Any


def dict_filter(filter_func: Callable[[Any, Any], bool], dictionary: dict) -> dict:
    """
    Filter a dict object with the filter function given.
    :filter_func: the function to filter with
    :dictionary: the dictionary to filter
    :return: the filtered dictionary
    """

    return {
        k: v for k, v in filter(
            lambda d: filter_func(d[0], d[1]),
            dictionary.items()
        )
    }


def dict_prefix(prefix: str, dictionary: dict) -> dict:
    """
    Take only the keys that start with the prefix, and remove this prefix from the keys.
    :prefix: the prefix to use
    :dictionary: the dictionary to filter
    :return: the dictionary with the prefix
    """

    return {
        k.removeprefix(prefix): v for k, v in dict_filter(
            lambda k, v: k.startswith(prefix),
            dictionary
        ).items()
    }
