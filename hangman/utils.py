from typing import Sequence


def find_all(sub: str, a_str: str) -> Sequence[int]:
    """
    Finds all the occurrences of `sub` in `a_str`. returns a list
    containing all of them. This should be moved somewhere else.
    """
    indices = []
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            break
        indices.append(start)
        start += len(sub)  # use start += 1 to find overlapping matches

    return indices
