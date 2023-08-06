from typing import List

def simple_search(term: str, items: List[str]):
    results = []

    for item in items:
        if item == term:
            results.append(item)

    return results
