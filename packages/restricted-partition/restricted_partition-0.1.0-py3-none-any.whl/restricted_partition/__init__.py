"""Restricted Integer partitions.

A restricted partition is the subset of an integer partition with only partitions at
or below a certain length.

:author: Shay Hill
:created: 2023-03-03
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Union


def iter_partition(n: int, max_len: Union[int, None] = None) -> Iterator[list[int]]:
    """Iteratate over partitions of n, optionally limited to max_len.

    :param n: integer to partition
    :param max_len: optional maximum length of partitions to yield, at least 1
    :yield: partitions as lists of summands (smallest to largest)
    :return: yields partitions as lists of summands (smallest to largest)
    :raise ValueError: if max_len is less than 1

        >>> list(iter_partitions(3))
        [[1, 1, 1], [1, 2], [3]]

    If max_len is specified, the first partition of max_len will be

    [1] * (max_len - 1) + [n - max_len + 1]

    Partitions after this might be longer than max_len. For example, if n=7 and
    max_len=3, the first partition found with len==3 will be [1, 1, 5], but the
    next partition will be [1, 2, 2, 2]. So, skip to [1, 1, 5] then filter the
    remaining partitions.
    """
    if n < 0:
        return
    if max_len is not None and max_len < 1:
        msg = f"max_len must be at least 1, not {max_len}"
        raise ValueError(msg)

    ps = [0] * (n + 1)
    if max_len is None or n < max_len:
        # standard asc
        yield from _accel_asc(ps, 1, n - 1)
        return

    # max_len < n, skip most of the larger partitions
    ps[: max_len - 1] = [1] * (max_len - 1)
    ps[max_len - 1] = n - max_len + 1
    yield ps[:max_len]
    remaining_partitions = _accel_asc(ps, max_len - 1, n - max_len)
    yield from (x for x in remaining_partitions if len(x) <= max_len)


def _accel_asc(ps: list[int], k: int, shortage: int) -> Iterator[list[int]]:
    """The fastest known way to generate integer partitions in Python.

    :param ps: list of summands
    :param k: index of largest summand
    :param shortage: sum of remaining summands
    :yield: integer partitions of n
    :return: None

    Found at https://jeromekelleher.net/generating-integer-partitions.html
    """
    while k != 0:
        # increment value one step to the left
        x = ps[k - 1] + 1
        k -= 1
        # fill until the sum can be reached with [x, x] or [x, shortage]
        while 2 * x <= shortage:
            ps[k] = x
            shortage -= x
            k += 1
        # add x, move shortage to the right
        k_plus_1 = k + 1
        k_plus_2 = k + 2
        while x <= shortage:
            ps[k] = x
            ps[k_plus_1] = shortage
            yield ps[:k_plus_2]
            x += 1
            shortage -= 1
        ps[k] = x + shortage
        shortage = x + shortage - 1
        yield ps[:k_plus_1]


__all__ = ["iter_partition"]
