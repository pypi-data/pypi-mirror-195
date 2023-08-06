from collections.abc import Sequence
from enum import Enum
import logging
from pathlib import Path
from typing import Mapping
from PIL import Image, ImageDraw, ImageFont
from skit._types import Real, Rect, Color, FreeTypeFont
from abc import ABC, abstractmethod


logger = logging.getLogger(__file__)


# some defaults for fallback
DEFAULT_FONT = ImageFont.truetype('Helvetica', 16)
DEFAULT_COLOR = 'black'
DEFAULT_THICKNESS = 1

class DrawCommand(Enum):
    TEXT = 'text'
    RECTANGLE = 'rect'
    IMAGE = 'image'


class CardManipulation(ABC):
    @abstractmethod
    def background(self, color: str): pass

    @abstractmethod
    def layout(self, name: str, rect: Rect): pass

    @abstractmethod
    def layouts(self, names: Sequence[str], rects: Sequence[Rect]): pass

    @abstractmethod
    def layouts_map(self, layouts: Mapping[str, Rect]): pass

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
    def image(
        self,
        image: Path,
        layout: str,
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
    
    def layouts(self, names: Sequence[str], rects: Sequence[Rect]):
        assert len(names) == len(rects), "mismatched names/rects arguments"
        
        for name, rect in zip(names, rects):
            self.layout(name, rect)

    def layouts_map(self, layouts: Mapping[str, Rect]):
        for name, rect in layouts.items():
            self.layout(name, rect)

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

    def image(self, image: Path, layout: str):
        if layout in self._layouts:
            logger.debug(f"adding image for {layout}")
            self._commands.append({
                'op': DrawCommand.IMAGE,
                'layout': layout,
                'image': image,
            })
        else:
            raise KeyError(f"missing layout '{layout}'")

    def render_png(self, filename: str):
        logger.debug(f"rendering {filename}")

        with Image.new('RGBA', (self._width, self._height), self._background) as im:
            d = ImageDraw.Draw(im)

            for cmd in self._commands:
                op = cmd.pop('op')
                match op:
                    case DrawCommand.TEXT:
                        self._render_png_text(d, **cmd)
                    case DrawCommand.RECTANGLE:
                        self._render_png_rectangle(d, **cmd)
                    case DrawCommand.IMAGE:
                        self._render_png_image(im, **cmd)
                    case _:
                        raise ValueError(cmd)

            im.save(filename)

    def _render_png_text(self, d, layout, text, color, font):
        logger.debug(f"rendering text '{text}' at {layout}")
        layout = self._layouts[layout]
        d.text(
            [layout['x'], layout['y']],
            text,
            fill=color if color else DEFAULT_COLOR,
            font=font if font else DEFAULT_FONT,
        )
    
    def _render_png_rectangle(self, d, layout, color, thickness):
        logger.debug(f"rendering rectangle on {layout}")
        layout = self._layouts[layout]
        d.rectangle(
            [
                layout['x'],
                layout['y'],
                layout['x'] + layout['width'],
                layout['y'] + layout['height'],
            ],
            outline=color if color else DEFAULT_COLOR,
            width=thickness if thickness else DEFAULT_THICKNESS,
        )

    def _render_png_image(self, im, layout, image):
        logger.debug(f"rendering image at {layout}")
        layout = self._layouts[layout]
        with Image.open(image) as art:
            im.alpha_composite(art, (layout['x'], layout['y']))
