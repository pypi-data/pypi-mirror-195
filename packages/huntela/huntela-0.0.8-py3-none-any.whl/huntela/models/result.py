from typing import TypedDict, Union


class Result(TypedDict):
    confidence: Union[int, float]
    index: int
    value: str
