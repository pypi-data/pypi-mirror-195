from typing import List

from .constants import SUPPORTED_ITEM_TYPES
from .models import Result
from .utils import default_checker


def binary_search(term: int, items: List[int]):
    raise NotImplementedError


def simple_search(term: SUPPORTED_ITEM_TYPES, items: List[SUPPORTED_ITEM_TYPES]):
    results = []

    for index in range(len(items)):
        item = items[index]
        match = default_checker(item, term)
        if match[0]:
            results.append(Result(index=index, value=item, confidence=match[1]))

    return results


def search_for_least_frequent_items(size: int, items: List[SUPPORTED_ITEM_TYPES]):
    raise NotImplementedError


def search_for_most_frequent_items(size: int, items: List[SUPPORTED_ITEM_TYPES]):
    raise NotImplementedError


def search_csv_file(filename: str, column: str, value: str):
    raise NotImplementedError
