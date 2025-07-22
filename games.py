import cards
from cards import Card, CardIds
from piles import Pile, NoCardsInPileException

DRAW: str = "draw"
DISCARD_LOOT_CARD: str = "discard"
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
    _verbosity_level: int

    def __init__(
        self,
        proficiency_bonus: int = DEFAULT_PROFICIENCY_BONUS,
        deck: Pile = None,
        hand: Pile = None,
        discard: Pile = None,
        verbosity_level: int = 0,
    ):
        self._verbosity_level = verbosity_level
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

    def get_hand_str(self, indent=0) -> str:
        to_return = [
            f"{' ' * indent}Current hand:",
            self._hand.get_show_str(indent=indent + 4),
        ]
        return "\n".join(to_return)

    def get_hand_card_ids(self) -> list[cards.CardIds]:
        return self._hand.get_all_ids()

    def get_discard_card_ids(self) -> list[cards.CardIds]:
        return self._discard.get_all_ids()

    def get_deck_card_ids(self) -> list[cards.CardIds]:
        return self._deck.get_all_ids()

    def discard_at(self, i: int) -> None:
        discarded_card = self._hand.remove_at(i)
        self._discard.insert_top(discarded_card)

    def discard_multiple(self, indices: list[int]) -> None:
        # remove from largest to smallest index so that earlier removals don't mess up
        # indexing for later removals
        indices = sorted(indices, reverse=True)
        # slightly inefficient because we do multiple passes, but we'll survive somehow.
        for index in indices:
            self.discard_at(index)

    def _discard_card_with_id(self, id_: CardIds) -> None:
        discarded_card = self._hand.remove_by_id(id_)
        self._discard.insert_top(discarded_card)

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
        elif action == DISCARD_LOOT_CARD:
            self._discard_card_with_id(CardIds.LOOT)
            for _ in range(2):
                self._game_action_stack.append(DRAW)
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
            try:
                self._recycle_discard()
            except CantDrawBecauseOfExceptionalCards:
                print(
                    f"    Cannot draw more cards because there are only weird cards left"
                )
                return
            card = self._deck.draw()
        self._hand.insert_right(card)
        self._on_draw(card)
        if self._verbosity_level >= 1:
            print(f"    Drew card: {card}")

    def _recycle_discard(self) -> None:
        if self._discard.only_has_exceptional_cards():
            raise CantDrawBecauseOfExceptionalCards()
        discards = self._discard.draw_all()
        for card in discards:
            self._deck.insert_top(card)
        self._deck.shuffle()

    def _on_draw(self, card: Card):
        match card.id:
            case cards.CardIds.LOOT:
                self._game_action_stack.append(DISCARD_LOOT_CARD)
            case cards.CardIds.PROFICIENT_DRAW:
                for _ in range(self._proficiency_bonus):
                    self._game_action_stack.append(DRAW)
            case _:
                pass

    def shuffle_deck(self) -> None:
        self._deck.shuffle()


class CantDrawBecauseOfExceptionalCards(Exception):
    pass
