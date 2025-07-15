import games
from cards import CardIds
import piles


def test_pile_print():
    deck = piles.get_pile_from_ids(
        [
            CardIds.ACTION,
            CardIds.STUNT,
            CardIds.MOVE,
            CardIds.STUNT,
            CardIds.DOUBLE_MOVE,
        ]
    )
    assert (
        str(deck)
        == """
0: Gain 1 Action.
1: Gain 1 Stunt.
2: Move # of spaces up to your speed.
3: Gain 1 Stunt.
4: Move # of spaces up to 2x your speed.
           """.strip()
    )


def test_basic_draw():
    deck = piles.get_pile_from_ids(
        [
            CardIds.ACTION,
            CardIds.ACTION,
        ]
    )
    game = games.GameState(deck=deck)
    game.draw_cards(1)
    assert game.get_hand_card_ids() == [CardIds.ACTION]


def test_trigger_shuffle_with_draw():
    deck = piles.get_pile_from_ids(
        [
            CardIds.ACTION,
            CardIds.ACTION,
        ]
    )
    discard = piles.get_pile_from_ids([CardIds.BOON])
    game = games.GameState(deck=deck, discard=discard)
    game.draw_cards(3)
    assert game.get_hand_card_ids() == [
        CardIds.ACTION,
        CardIds.ACTION,
        CardIds.BOON,
    ]


def test_drawing_when_deck_and_discard_are_empty():
    deck = piles.Pile([])
    discard = piles.Pile([])
    game = games.GameState(deck=deck, discard=discard)
    game.draw_cards(1)
    assert game.get_hand_card_ids() == []


def test_drawing_proficiency_bonus():
    deck = piles.get_pile_from_ids(
        [
            CardIds.PROFICIENT_DRAW,
            CardIds.BOON,
            CardIds.BOON,
            CardIds.BOON,
            CardIds.BOON,
            CardIds.BOON,
        ]
    )
    game = games.GameState(deck=deck, proficiency_bonus=3)
    game.draw_cards(1)
    hand_card_ids = game.get_hand_card_ids()
    assert hand_card_ids == [
        CardIds.PROFICIENT_DRAW,
        CardIds.BOON,
        CardIds.BOON,
        CardIds.BOON,
    ]


def test_discard():
    hand = piles.get_pile_from_ids(
        [
            CardIds.BOON,
            CardIds.ACTION,
            CardIds.REACT,
            CardIds.SPRINT,
        ]
    )
    game = games.GameState(hand=hand)

    game.discard_at(1)

    assert game.get_discard_card_ids() == [CardIds.ACTION]
    assert game.get_hand_card_ids() == [
        CardIds.BOON,
        CardIds.REACT,
        CardIds.SPRINT,
    ]
