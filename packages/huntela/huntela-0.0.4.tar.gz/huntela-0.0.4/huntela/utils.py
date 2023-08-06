from collections import Counter
import itertools

from .constants import SUPPORTED_ITEM_TYPES


def default_checker(item_1: SUPPORTED_ITEM_TYPES, item_2: SUPPORTED_ITEM_TYPES):
    if item_1 == item_2:
        return (True, 1)

    if type(item_1) is str and type(item_2) is str and (len(item_1) > 1 or len(item_2) > 1):
        item_1_char_count = char_count(item_1)
        item_2_char_count = char_count(item_2)

        combined_chars = set()

        unconsumed_chars = 0
        total_chars = 0

        for char in item_1_char_count:
            combined_chars.add(char)
        for char in item_2_char_count:
            combined_chars.add(char)

        for char in combined_chars:
            count_in_item_1 = item_1_char_count[char] if char in item_1_char_count else 0
            count_in_item_2 = item_2_char_count[char] if char in item_2_char_count else 0

            combined_count = count_in_item_1 + count_in_item_2

            unconsumed_chars += abs(count_in_item_1 - count_in_item_2)
            total_chars += combined_count

        percentage_match = 1 - (unconsumed_chars / max(len(item_1), len(item_2)))
        if percentage_match > 0.5:
            return (True, round(percentage_match, 1))

    return (False, None)


def char_count(s):
    """
    Returns a dictionary mapping each character in a string to the number of times it appears.

    Args:
        s (str): Input string.

    Returns:
        dict: Dictionary mapping each character to the number of times it appears.
    """

    char_dict = {}
    for char, count in Counter(itertools.chain.from_iterable(s)).items():
        char_dict[char] = count

    return char_dict
