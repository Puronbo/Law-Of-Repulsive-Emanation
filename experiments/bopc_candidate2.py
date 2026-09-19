"""
BOPC candidate #2: Selection sort on 8 elements.
Resource: comparisons (exact, data-independent).
Bound: exactly 28 comparisons for 8 inputs (n*(n-1)/2).
Semantics: output must be sorted ascending; byte-identical to Python's sorted().
"""

from typing import List, Tuple


def sort8_ref(arr: List[int]) -> Tuple[int, ...]:
    """Reference: Python's sorted (correct-or-raise)."""
    return tuple(sorted(arr))


def sort8_counted(arr: List[int]) -> Tuple[Tuple[int, ...], int]:
    """Selection sort on 8 elements with comparison counting.
    Returns (sorted_tuple, comparisons).
    """
    a = list(arr)  # copy
    n = len(a)
    comparisons = 0
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
    return tuple(a), comparisons


def bound_for(n: int) -> int:
    """Proven bound: n*(n-1)/2 comparisons for selection sort."""
    if n != 8:
        raise ValueError("This candidate only handles 8-element arrays")
    return 28  # 8*7/2 = 28