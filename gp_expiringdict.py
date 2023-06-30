# enable new style type annotation (default from Python 3.9 on)
from __future__ import annotations

import itertools
from threading import RLock
from time import time, sleep
from unittest import TestCase

ASSIGNMENT_TTL_SEC = 1.0


class GPExpiringDict:
    """
    GPExpiringDict class.

    A simple structure for creating a dictionary which supports ttl.
    """

    class Entry:
        """
        Entry class.

        The value implementation of the GPExpiringDict.
        """

        def __init__(self, value, ttl=ASSIGNMENT_TTL_SEC):
            """Entry class initializer method"""

            self.value = value
            self.expires_at = time() + ttl

        def expired(self):
            """
            expired instance method.

            Takes instance, Returns a boolean that indicates the entry is
            expired or not.
            """

            return self.expires_at < time()

    def __init__(self):
        """GPExpiringDict class initializer method"""

        self.entries = {}
        self.lock = RLock()

    def set_value(self, key, value, ttl=ASSIGNMENT_TTL_SEC):
        """
        Public setter.

        :param str key: Compound name in this example
        :param tuple value: Color that is going to be assigned to a compound.
        :param int ttl: expiration in seconds.

        :return: None
        """

        with self.lock:
            self.entries[key] = self.Entry(value, ttl)

    def get_value(self, key):
        """
        Public getter.

        :param str key: Compound name in this example.
        :return: The assigned color to the compound
        """

        with self.lock:
            item = self.entries[key]

            if time() < item.expires_at:
                return item.value
            else:
                del self.entries[key]
                raise KeyError(key)

    def read_unexpired_entries(self):
        """Public read assignments method"""

        with self.lock:
            unexpired = itertools.dropwhile(
                lambda entry: entry[1].expired(),
                self.entries.items()
            )
            assignments = {
                entry[0]: entry[1].value for entry in unexpired
            }

            return assignments


_compound_colors = GPExpiringDict()


def color_for_compound(compound: str) -> tuple[float, float, float]:
    """
    Returns a color to display the given 'compound' in an image.
    Will always return the same value for a compound.
    When a compound is seen the first time, the next available color
    form a pre-defined pallet is assigned.

    Each assignment is deleted after it was not used for ASSIGNMENT_TTL_SEC

    """

    compound_color = None
    try:
        compound_color = _compound_colors.get_value(compound)
    except KeyError:
        for color in _palette:
            if color not in _compound_colors.read_unexpired_entries().values():
                compound_color = color
                break
    finally:
        _compound_colors.set_value(compound, compound_color)

    return compound_color


def get_compound_to_color_assignments() -> dict:
    """
    Returns a dict containing all known compound -> color assignments.
    May be used to render a legend.

    Example return value: {
                            "Aceton" : (0.9, 0.0, 0.04),
                            "Benzol" : (0.54, 0.16, 0.8)
                          }

    """

    return _compound_colors.read_unexpired_entries()


# this palette is developed based on seaborn's 'color_palette()''
# function - please do not edit

_palette = [
    (0.9, 0.0, 0.04),
    (0.54, 0.16, 0.8),
    (1.0, 0.48, 0.0),
    (0.94, 0.29, 0.75),
    (0.1, 0.78, 0.21)
]

"""

   Test case - please do not edit

"""

if __name__ == '__main__':
    tc = TestCase()

    tc.assertEqual(
        color_for_compound("Ammoniak"),
        (0.9, 0.0, 0.04)
    )  # first color from _palette

    tc.assertEqual(
        color_for_compound("Benzol"),
        (0.54, 0.16, 0.8)
    )  # second color from _palette

    tc.assertEqual(
        color_for_compound("Aceton"),
        (1.0, 0.48, 0.0)
    )  # third color from _palette

    sleep(0.7)

    tc.assertEqual(
        color_for_compound("Benzol"),
        (0.54, 0.16, 0.8)
    )  # second color from _palette

    # all assignments except for "Benzol" will expire during this sleep
    sleep(0.7)

    tc.assertEqual(
        color_for_compound("Benzol"),
        (0.54, 0.16, 0.8)
    )  # second color from _palette

    tc.assertEqual(
        color_for_compound("Aceton"),
        (0.9, 0.0, 0.04)
    )  # first color from _palette

    print(get_compound_to_color_assignments())
