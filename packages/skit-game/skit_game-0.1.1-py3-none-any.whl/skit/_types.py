from typing import NamedTuple, NewType
from numbers import Real
from PIL.ImageFont import FreeTypeFont

class Rect(NamedTuple):
    x: Real
    y: Real
    width: Real
    height: Real

# color - thin wrapper on str right now, and there are only
# some forms that PIL allows, so this should be smarter one day
# https://pillow.readthedocs.io/en/stable/reference/ImageColor.html
Color = NewType('Color', str)

__all__ = [
    'Real',
    'FreeTypeFont',
    'Rect',
    'Color',
]