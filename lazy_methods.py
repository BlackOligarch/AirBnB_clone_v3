#!/usr/bin/python3

"""
This module provides methods for various operations.
"""


def empty_object_dictionary(objects_dict: dict) -> None:
    """
    Empties the given dictionary by removing all key-value pairs.

    Args:
        objects_dict (dict): The dictionary to be emptied.
    """
    for key in list(objects_dict.keys()):
        del objects_dict[key]
