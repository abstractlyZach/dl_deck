import games
import cards

def test_pile_print():
    mydeck = games.Pile([cards.Action(), cards.Action()])
    assert str(mydeck) == \
"""
0: Gain 1 Action.
1: Gain 1 Action.
""".strip()

def test_basic_draw():
    deck = games.Pile([cards.Action(), cards.Action()])
    game = games.GameState(deck=deck)
    game.draw_cards(1)
    # todo: actually check the hand by adding hand checking
    assert game.get_hand_str() == "0: Gain 1 Action."

def test_trigger_shuffle_with_draw():
    deck = games.Pile([cards.Action(), cards.Action()])
    discard = games.Pile([cards.Boon()])
    game = games.GameState(deck=deck, discard=discard)
    game.draw_cards(3)
    # todo: actually check the hand by adding hand checking
    assert game.get_hand_str() == "0: Gain 1 Action.\n1: Gain 1 Action.\n2: Boon."

def test_drawing_when_deck_and_discard_are_empty():
    deck = games.Pile([])
    discard = games.Pile([])
    game = games.GameState(deck=deck, discard=discard)
    game.draw_cards(1)
    assert game.get_hand_str() == ""