from collections import Counter
import itertools
from typing import Dict, List, Set, Tuple, Union

from .constants import SUPPORTED_ITEM_TYPES


def default_checker(item_1: SUPPORTED_ITEM_TYPES, item_2: SUPPORTED_ITEM_TYPES) -> Tuple[bool, Union[float, int]]:
    if item_1 == item_2:
        return (True, 1)

    if type(item_1) is str and type(item_2) is str and (len(item_1) > 1 or len(item_2) > 1):
        char_counts, combined_chars = char_count([item_1, item_2])

        unconsumed_chars = 0
        total_chars = 0

        for char in combined_chars:
            count_in_item_1 = char_counts[0][char] if char in char_counts[0] else 0
            count_in_item_2 = char_counts[1][char] if char in char_counts[1] else 0

            combined_count = count_in_item_1 + count_in_item_2

            unconsumed_chars += abs(count_in_item_1 - count_in_item_2)
            total_chars += combined_count

        percentage_match = 1 - (unconsumed_chars / max(len(item_1), len(item_2)))
        if percentage_match > 0.5:
            return (True, round(percentage_match, 1))

    return (False, None)


def char_count(items: List[str]) -> Tuple[List[Dict[str, int]], Set[str]]:
    """
    Returns a dictionary mapping each character in a string to the number of times it appears.

    Args:
        s (str): Input string.

    Returns:
        dict: Dictionary mapping each character to the number of times it appears.
    """

    results = []
    combined_chars = set()

    for item in items:
        char_dict = {}
        for char, count in Counter(itertools.chain.from_iterable(item)).items():
            char_dict[char] = count
            combined_chars.add(char)

        results.append(char_dict)

    return (results, combined_chars)


def cleanup_string(s: str) -> str:
    """
    Cleans up a string by removing any leading or trailing white space characters.
    
    Args:
        s (str): The string to be cleaned up.
        
    Returns:
        str: A new string with no leading or trailing white space characters.
    """

    return s.strip()
