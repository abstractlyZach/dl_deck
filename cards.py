class OnCardDrawAction:
    pass


class DoNothing(OnCardDrawAction):
    pass


class Card:
    _id: int
    _name: str
    _description: str

    def __repr__(self):
        return f"{self._name}"

    def __str__(self):
        return f"{self._description}"

    def on_draw(self) -> OnCardDrawAction:
        return DoNothing()

    def __eq__(self, other):
        return self._id == other._id


class Action(Card):
    _id = 0
    _name = ""
    _description = "Gain 1 Action."


class Stunt(Card):
    _id = 1
    _name = ""
    _description = "Gain 1 Stunt."


class Move(Card):
    _id = 2
    _name = ""
    _description = "Move # of spaces up to your speed."


class React(Card):
    _id = 3
    _name = ""
    _description = "Gain 1 Reaction."


class DoubleMove(Card):
    _id = 4
    _name = ""
    _description = "Move # of spaces up to 2x your speed."


class Loot(Card):
    _id = 5
    _name = ""
    _description = "Discard this card, draw 2 cards"


class Sprint(Card):
    _id = 6
    _name = ""
    _description = "Move # of spaces up to your speed, draw 1 card."


class SuperReact(Card):
    _id = 7
    _name = ""
    _description = "Gain 1 Reaction, draw 2 cards."


class ProficientDraw(Card):
    _id = 8
    _name = ""
    _description = "Draw a # of cards = proficiency bonus."


class Boon(Card):
    _id = 9
    _name = ""
    _description = "Boon."
