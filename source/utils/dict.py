from typing import Callable, Any


def dict_filter(filter_func: Callable[[Any, Any], bool], dictionary: dict[Any, Any]) -> dict[Any, Any]:
    """
    Filter a dict object with the filter function given.
    :param filter_func: the function to filter with
    :param dictionary: the dictionary to filter
    :return: the filtered dictionary

    Example :
    filter_func = lambda key, value: key.startswith("valeur")
    dictionary = {"valeur1": 1, "valeur2": 2, "clé1": None}

    result = {"valeur1": 1, "valeur2": 2}

    """

    return {
        k: v for k, v in filter(
            lambda d: filter_func(d[0], d[1]),
            dictionary.items()
        )
    }


def dict_filter_prefix(prefix: str, dictionary: dict[str, Any]) -> dict[str, Any]:
    """
    Take only the keys that start with the prefix, and remove this prefix from the keys.
    :param prefix: the prefix to use
    :param dictionary: the dictionary to filter
    :return: the dictionary with the prefix

    Example:
    prefix = "button"
    dictionary = {"button1": 1, "button2": 2, "label1": None}

    result = {"1": 1, "2": 2}
    """

    return {
        k.removeprefix(prefix): v for k, v in dict_filter(
            lambda k, v: k.startswith(prefix),
            dictionary
        ).items()
    }


def dict_add_prefix(prefix: str, dictionary: dict[str, Any]) -> dict[str, Any]:
    """
    Add a prefix to every key of the dictionary
    :param prefix: the prefix to add
    :param dictionary: the dictionary to modify
    :return: the dictionary with the prefix at the start of the keys
    """

    return {
        prefix + k: v
        for k, v in dictionary.items()
    }
