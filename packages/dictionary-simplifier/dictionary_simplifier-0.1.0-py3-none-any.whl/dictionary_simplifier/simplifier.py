from collections.abc import MutableMapping
from typing import Any, Dict


def flatten_dict(
    d: Dict[str, Any], parent_key: str = "", sep: str = "_"
) -> Dict[str, Any]:
    """
    Flatten a nested dictionary by joining the keys with the
    specified separator.
    Args:
        d (dict): A nested dictionary to flatten
        parent_key (str, optional): The parent key to use when joining keys.
        Defaults to ''.
        sep (str, optional): The separator to use when joining keys.
        Defaults to '_'.

    Returns:
        dict: A flattened dictionary where keys are the joined paths to
        each value, and values are the corresponding values.
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                items.extend(flatten_dict({str(i): item}, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_value_by_key_path(d: dict, key_path: str) -> any:
    """
    Given a nested dictionary and a key path, returns the value corresponding
    to the key path.

    Args:
        d (dict): The dictionary to extract the value from.
        key_path (str): The path to the key to extract, separated by '.'.

    Returns:
        any: The value of the key at the specified path, or None if the key
             does not exist.

    Example:
        >>> d = {'a': {'b': {'c': 1}}}
        >>> get_value_by_key_path(d, 'a.b.c')
        1
    """
    keys = key_path.split(".")
    value = d
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        elif isinstance(value, list) and key.isdigit() and int(key) < len(value):
            value = value[int(key)]
        else:
            return None
    return value
