from typing import List, Optional

from .constants import SUPPORTED_ITEM_TYPES
from .models import Result
from .utils import cleanup_string, default_checker


def binary_search(term: SUPPORTED_ITEM_TYPES, items: List[SUPPORTED_ITEM_TYPES]) -> Optional[Result]:
    """
    Performs a binary search on a list of integers to find a target value.

    Args:
        term: The target integer to search for.
        items: The list of integers to search through.

    Returns:
        The index of the target value in the list, or None if it is not found.
    """

    left, right = 0, len(items) - 1

    while left <= right:
        mid = (left + right) // 2
        if items[mid] == term:
            return Result(confidence=1, index=mid, value=term)
        elif items[mid] > term:
            right = mid - 1
        else:
            left = mid + 1

    return None


def simple_search(term: SUPPORTED_ITEM_TYPES, items: List[SUPPORTED_ITEM_TYPES]) -> List[Result]:
    f"""
    Searches a list of items for a given search term.

    Args:
        term ({SUPPORTED_ITEM_TYPES}): The search term to match against items in the list.
        items ({List[SUPPORTED_ITEM_TYPES]}): The list of items to search.

    Returns:
        {List[Result]}: A list of Result objects representing the search results.
    """

    results = []

    for index in range(len(items)):
        item = items[index]

        if type(item) is str:
            item = cleanup_string(item)

        match = default_checker(item, term)
        if match[0]:
            results.append(Result(index=index, value=item, confidence=match[1]))

    results.sort(key=lambda x: x['confidence'])

    return results


def search_for_least_frequent_items(size: int, items: List[SUPPORTED_ITEM_TYPES]):
    raise NotImplementedError


def search_for_most_frequent_items(size: int, items: List[SUPPORTED_ITEM_TYPES]):
    raise NotImplementedError


def search_csv_file(filename: str, column: str, value: str):
    raise NotImplementedError
