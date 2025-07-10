import game
import cards

def test_basic_draw():
    mydeck = game.Pile([cards.Action(), cards.Action()])
    mygame = game.GameState(deck=mydeck)
    mygame.draw_cards(1)
    # todo: actually check the hand by adding hand checking
    assert mygame.get_hand_str() == "ab"

