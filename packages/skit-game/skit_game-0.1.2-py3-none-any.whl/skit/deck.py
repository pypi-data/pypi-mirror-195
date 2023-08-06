from collections.abc import MutableSequence, Sequence
import logging
from pathlib import Path
from typing import Self, Mapping
import warnings
from skit.card import Card, CardManipulation
from skit._types import Real, Rect, Color, FreeTypeFont


logger = logging.getLogger(__file__)

class Deck(MutableSequence, CardManipulation):
    def __init__(self, card_count: int = 1, width: int | None = None, height: int | None = None):
        opts = {}
        if width: opts['width'] = width
        if height: opts['height'] = height
        self._cards: list[Card] = [Card(**opts) for _ in range(card_count)]
    
    #region MutableSequence
    def __getitem__(self, index):
        return self._cards[index]
    
    def __delitem__(self, index):
        del self._cards[index]
    
    def __iter__(self):
        return self._cards.__iter__()

    def __len__(self) -> int:
        return len(self._cards)
    
    def __setitem__(self, index, value):
        self._cards[index] = value
    
    def insert(self, index, value):
        self._cards.insert(index, value)
    #endregion

    #region Container convenience
    def __add__(self, other: Self) -> Self:
        if not issubclass(type(other), Deck):
            raise NotImplemented

        d = Deck(0)
        d._cards = self._cards + other._cards
        return d
    #endregion

    #region Card manipulation
    def background(self, color: str):
        logger.debug(f"Deck.background({color})")
        for card in self._cards:
            card.background(color)
    
    def layout(self, name: str, rect: Rect):
        logger.debug(f"Deck.layout({name}, ...)")
        for card in self._cards:
            card.layout(name, rect)
    
    def layouts(self, names: Sequence[str], rects: Sequence[Rect]):
        logger.debug(f"Deck.layouts(sequence of layouts)")
        for card in self._cards:
            card.layouts(names, rects)

    def layouts_map(self, layouts: Mapping[str, Rect]):
        logger.debug(f"Deck.layouts_map(map of name->layouts)")
        for card in self._cards:
            card.layouts_map(layouts)

    def text(self, text: str, layout: str, font: FreeTypeFont | None = None, color: Color | None = None):
        logger.debug(f"Deck.text({text})")
        for card in self._cards:
            card.text(text, layout, font, color)
    
    def rectangle(self, layout: str, color: Color | None = None, thickness: Real | None = None):
        logger.debug(f"Deck.rect({layout})")
        for card in self._cards:
            card.rectangle(layout, color, thickness)

    def image(self, image: Path, layout: str):
        logger.debug(f"Deck.image({image})")
        for card in self._cards:
            card.image(layout, image, layout)

    def render_png(self, filename: str):
        logger.debug(f"Deck.render_png({filename})")

        if '{index}' not in filename:
            warnings.warn("'{index}' isn't in the filename, so images may overwrite one another")

        for index, card in enumerate(self._cards):
            card.render_png(filename.format_map({
                'index': index,
            }))
    #endregion

    #region Card sequence manipulation
    def backgrounds(self, colors: Sequence[str]):
        logger.debug(f"Deck.backgrounds(sequence of colors)")
        for card, color in zip(self._cards, colors):
            card.background(color)

    def texts(self, texts: Sequence[str], layout: str, font: FreeTypeFont | None = None, color: Color | None = None):
        logger.debug(f"Deck.texts(sequence of strings)")
        for card, text in zip(self._cards, texts):
            card.text(text, layout, font, color)

    def images(self, images: Sequence[Path], layout: str):
        logger.debug(f"Deck.images(sequence of images)")
        for card, image in zip(self._cards, images):
            card.image(layout, image, layout)
    #endregion

    def __str__(self):
        return ", ".join([f"{idx}: {c}" for idx, c in enumerate(self._cards)])
