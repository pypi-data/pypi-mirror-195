from .deck import Deck
from .card import Card
from ._types import Rect, Color

from PIL import ImageFont


# expose ImageFont.truetype() as skit.load_font()
load_font = ImageFont.truetype


# helper for parsing layouts from JSON
def json_layout_hook(incoming_dict: dict) -> dict | Rect:
    match incoming_dict:
        case { 'x': _, 'y': _, 'width': _, 'height': _, **rest } if len(rest) == 0:
            return Rect(**incoming_dict)
        case _:
            return incoming_dict
