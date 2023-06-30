# enable new style type annotation (default from Python 3.9 on)
from __future__ import annotations

from time import sleep
from unittest import TestCase

from expiringdict import ExpiringDict

ASSIGNMENT_TTL_SEC = 1.0
_compound_colors = ExpiringDict(max_len=4, max_age_seconds=ASSIGNMENT_TTL_SEC)


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
        compound_color = _compound_colors[compound]
    except KeyError:
        for color in _palette:
            if color not in _compound_colors.values():
                compound_color = color
                break
    finally:
        _compound_colors[compound] = compound_color

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

    return dict(_compound_colors.items())


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
