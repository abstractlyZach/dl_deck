import random
from typing import Iterable
from collections import deque

import cards
from cards import Card, CardIds


class Pile:
    """A collection of Cards

    - Top of Pile is the 0th index
    - Bottom of Pile is the largest index
    - This means that you can pass an ordered list and expect cards to be
       drawn in the same order of the list
    """

    _cards: deque[Card]

    def __init__(self, _cards=None):
        if not _cards:
            _cards = []
        self._cards = deque(_cards)

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
        return self._cards.popleft()

    def draw_all(self) -> Iterable[Card]:
        yield self._cards.popleft()

    def get_all_ids(self) -> list[CardIds]:
        return [card.id for card in self._cards]

    def insert_top(self, card: Card) -> None:
        self._cards.appendleft(card)

    def insert_bottom(self, card: Card) -> None:
        self._cards.append(card)

    def insert_left(self, card: Card) -> None:
        """Some piles like to be displayed left to right, like the hand."""
        self.insert_top(card)

    def insert_right(self, card: Card) -> None:
        """Some piles like to be displayed left to right, like the hand."""
        self.insert_bottom(card)

    def remove_at(self, i: int) -> Card:
        if not (0 < i < self.size()):
            raise Exception(
                f"Cannot remove card at index {i} in a Pile of size {self.size()}"
            )
        # deques don't support arbitrary index removal, so we do it ourselves
        self._cards.rotate(-i)
        removed_card = self._cards.popleft()
        self._cards.rotate(i)
        return removed_card


class NoCardsInPileException(RuntimeError):
    pass


def get_pile_from_ids(ids: Iterable[CardIds]) -> Pile:
    return Pile([cards.get_card_from_id(_id) for _id in ids])
