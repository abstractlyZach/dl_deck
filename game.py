import random

from collections.abc import Callable

from cards import Card


class Pile:
    """A collection of Cards"""

    # Top of Pile is the largest index
    # Bottom of Pile is the 0th index.
    _cards: list[Card]

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


class GameState:
    """Manager of the game's state.

    Any class that has a trigger or an action must do so through this class.
    """
    _deck: Pile
    _hand: Pile
    _discard: Pile
    _action_stack: list[Callable]

    def __init__(self, deck: Pile = None, hand: Pile = None, discard: Pile = None):
        if not deck:
            deck = []
        self._deck = deck

        if not hand:
            hand = []
        self._hand = hand

        if not discard:
            discard = []
        self._discard = discard

        self._action_stack = []

    def return_all_cards(self):
        for pile in [self._hand, self._discard]:
            for _ in range(pile.size()):
                card = pile.draw()
                self._deck.insert_top(card)
        self._deck.shuffle()
        
    def get_hand_str(self)->str:
        return str(self._hand)

    def draw_cards(self, x:int)->None:
        self._action_stack = [self._deck.draw for _ in range(x)]
        self._process_action_stack()

    def _process_action_stack(self)->None:
        while self._action_stack:
            action = self._action_stack.pop()
            effect = action()
            if effect.iscard():
                effect.ondraw()

