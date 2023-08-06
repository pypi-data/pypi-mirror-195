from enum import Enum
import logging
from PIL import Image, ImageDraw, ImageFont
from skit._types import Real, Rect, Color, FreeTypeFont
from abc import ABC, abstractmethod


logger = logging.getLogger(__file__)


class DrawCommand(Enum):
    TEXT = 'text'
    RECTANGLE = 'rect'


class CardManipulation(ABC):
    @abstractmethod
    def background(self, color: str): pass

    @abstractmethod
    def layout(self, name: str, rect: Rect): pass

    @abstractmethod
    def text(
        self, text: str,
        layout: str,
        font: FreeTypeFont | None = None,
        color: Color | None = None,
    ): pass

    @abstractmethod
    def rectangle(
        self,
        layout: str,
        color: Color | None = None,
        thickness: Real | None = None,
    ): pass

    @abstractmethod
    def render_png(self, filename: str): pass


class Card(CardManipulation):
    def __init__(self, width: int = 750, height: int = 1050):
        self._width = width
        self._height = height
        self._layouts = {}
        self._background = '#ffffff00'
        self._commands = []

    def background(self, color: str):
        assert type(color) is str

        logger.debug(f"setting background to {color}")
        self._background = color

    def layout(self, name: str, rect: Rect):
        logger.debug(f"creating layout area {name}")
        self._layouts[name] = {
            'x': rect.x,
            'y': rect.y,
            'width': rect.width,
            'height': rect.height,
        }
    
    def text(self, text: str, layout: str, font: FreeTypeFont | None = None, color: Color | None = None):
        assert type(text) is str

        if layout in self._layouts:
            logger.debug(f"adding '{text}' in {layout}")
            self._commands.append({
                'op': DrawCommand.TEXT,
                'layout': layout,
                'text': text,
                'font': font,
                'color': color,
            })
        else:
            raise KeyError(f"missing layout '{layout}'")

    def rectangle(self, layout: str, color: Color | None = None, thickness: Real | None = None):
        if layout in self._layouts:
            logger.debug(f"adding rectangle for {layout}")
            self._commands.append({
                'op': DrawCommand.RECTANGLE,
                'layout': layout,
                'color': color,
                'thickness': thickness,
            })
        else:
            raise KeyError(f"missing layout '{layout}'")

    def render_png(self, filename: str):
        logger.debug(f"rendering {filename}")

        # some defaults for fallback
        default_font = ImageFont.truetype('Helvetica', 16)
        default_color = 'black'
        default_thickness = 1

        with Image.new('RGBA', (self._width, self._height), self._background) as im:
            d = ImageDraw.Draw(im)

            for cmd in self._commands:
                match cmd:
                    case {'op': DrawCommand.TEXT, 'layout': layout, 'text': text, 'font': font, 'color': color}:
                        logger.debug(f"rendering text '{text}' at {layout}")
                        layout = self._layouts[layout]
                        d.text(
                            [layout['x'], layout['y']],
                            text,
                            fill=color if color else default_color,
                            font=font if font else default_font,
                        )
                    case {'op': DrawCommand.RECTANGLE, 'layout': layout, 'color': color, 'thickness': thickness}:
                        logger.debug(f"rendering rectangle on {layout}")
                        layout = self._layouts[layout]
                        d.rectangle(
                            [
                                layout['x'],
                                layout['y'],
                                layout['x'] + layout['width'],
                                layout['y'] + layout['height'],
                            ],
                            outline=color if color else default_color,
                            width=thickness if thickness else default_thickness,
                        )
                    case _:
                        raise ValueError(cmd)

            im.save(filename)
