from typing import Iterable

import cards
from cards import Card, Loot, ProficientDraw
from piles import Pile, NoCardsInPileException

DRAW: str = "draw"
DISCARD: str = "discard"
DEFAULT_PROFICIENCY_BONUS: int = 4


class GameState:
    """Manager of the game's state.

    Any class that has a trigger or an action must do so through this class.
    """
    _deck: Pile
    _hand: Pile
    _discard: Pile
    _proficiency_bonus: int
    _game_action_stack: list[str]

    def __init__(self, proficiency_bonus: int = DEFAULT_PROFICIENCY_BONUS, deck: Pile = None, hand: Pile = None,
                 discard: Pile = None):
        if not deck:
            deck = Pile()
        self._deck = deck

        if not hand:
            hand = Pile()
        self._hand = hand

        if not discard:
            discard = Pile()
        self._discard = discard

        self._game_action_stack = []
        self._proficiency_bonus = proficiency_bonus

    def return_all_cards(self):
        for pile in [self._hand, self._discard]:
            for _ in range(pile.size()):
                card = pile.draw()
                self._deck.insert_top(card)
        self._deck.shuffle()

    def get_hand_str(self) -> str:
        return str(self._hand)

    def get_hand_card_ids(self) -> Iterable[cards.CardIds]:
        return self._hand.get_all_ids()

    def draw_cards(self, x: int) -> None:
        for _ in range(x):
            self._game_action_stack.append(DRAW)
        self._process_stack()

    def _process_stack(self):
        while self._game_action_stack:
            self._process_next_action()

    def _process_next_action(self):
        if not self._game_action_stack:
            raise Exception("Tried to process stack but it was empty")
        action = self._game_action_stack.pop()
        if action == DRAW:
            self._draw_card()
        elif action == DISCARD:
            # The only discard
            pass
        else:
            raise Exception("unrecognized game action")

    def _draw_card(self) -> None:
        # Make sure that recycling the discard pile will give us a possible draw
        if self._discard.size() <= 0 and self._deck.size() <= 0:
            # do nothing
            return

        try:
            card = self._deck.draw()
        except NoCardsInPileException:
            self._recycle_discard()
            card = self._deck.draw()
        self._hand.insert_top(card)
        self._on_draw(card)

    def _recycle_discard(self) -> None:
        discards = self._discard.draw_all()
        for card in discards:
            self._deck.insert_top(card)
        self._deck.shuffle()

    def _on_draw(self, card: Card):
        match card._id:
            case Loot._id:
                self._game_action_stack.append(DISCARD)
            case ProficientDraw._id:
                for _ in range(self._proficiency_bonus):
                    self._game_action_stack.append(DRAW)
            case _:
                pass
