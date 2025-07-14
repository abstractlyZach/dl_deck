import random
from typing import Iterable

import cards
from cards import Card, CardIds


class Pile:
    """A collection of Cards"""

    # Top of Pile is the largest index
    # Bottom of Pile is the 0th index.
    _cards: list[Card]

    def __init__(self, _cards=None):
        if not _cards:
            _cards = []
        self._cards = _cards

    def __str__(self):
        text_lines = []
        for i, card in enumerate(self._cards):
            text_lines.append(f"{i}: {card}")
        return "\n".join(text_lines)

    def empty(self) -> bool:
        return not self._cards

    def size(self) -> int:
        return len(self._cards)

    def shuffle(self):
        random.shuffle(self._cards)

    def draw(self) -> Card:
        if not self._cards:
            raise NoCardsInPileException("Attempted to draw from an empty Pile.")
        return self._cards.pop()

    def draw_all(self) -> Iterable[Card]:
        yield self._cards.pop()

    def get_all_ids(self) -> Iterable[CardIds]:
        return [card._id for card in self._cards]

    def insert_x_from_bottom(self, card: Card, x: int) -> None:
        """Inserts the card x away from the bottom of the Pile.
        """
        self._cards.insert(x, card)

    def insert_top(self, card: Card) -> None:
        self._cards.append(card)

    def insert_bottom(self, card: Card) -> None:
        self.insert_x_from_bottom(card, 0)


class NoCardsInPileException(RuntimeError):
    pass


def get_pile_from_ids(ids: Iterable[CardIds]) -> Pile:
    return Pile(
        [
            cards.get_card_from_id(_id)
            for _id in ids
        ]
    )
