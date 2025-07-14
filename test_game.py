import games
import cards


def test_pile_print():
    deck = games.get_pile_from_ids([
        cards.CardIds.ACTION,
        cards.CardIds.ACTION,
    ])
    assert str(deck) == \
           """
0: Gain 1 Action.
1: Gain 1 Action.
           """.strip()


def test_basic_draw():
    deck = games.get_pile_from_ids([
        cards.CardIds.ACTION,
        cards.CardIds.ACTION,
    ])
    game = games.GameState(deck=deck)
    game.draw_cards(1)
    assert game.get_hand_card_ids() == [
        cards.CardIds.ACTION
    ]


def test_trigger_shuffle_with_draw():
    deck = games.get_pile_from_ids([
        cards.CardIds.ACTION,
        cards.CardIds.ACTION,
    ])
    discard = games.get_pile_from_ids([
        cards.CardIds.BOON
    ])
    game = games.GameState(deck=deck, discard=discard)
    game.draw_cards(3)
    assert game.get_hand_card_ids() == [
        cards.CardIds.ACTION,
        cards.CardIds.ACTION,
        cards.CardIds.BOON,
    ]


def test_drawing_when_deck_and_discard_are_empty():
    deck = games.Pile([])
    discard = games.Pile([])
    game = games.GameState(deck=deck, discard=discard)
    game.draw_cards(1)
    assert game.get_hand_card_ids() == []
