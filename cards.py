import enum


class CardIds(enum.Enum):
    ACTION = 0
    STUNT = 1
    MOVE = 2
    REACT = 3
    DOUBLE_MOVE = 4
    LOOT = 5
    SPRINT = 6
    SUPER_REACT = 7
    PROFICIENT_DRAW = 8
    BOON = 9


class Card:
    _id: CardIds
    _name: str
    _description: str

    @property
    def id(self) -> CardIds:
        return self._id

    def __repr__(self):
        return f"{self._name}"

    def __str__(self):
        return f"{self._description}"

    def __eq__(self, other):
        if isinstance(other, Card):
            return self._id == other._id
        return NotImplemented


class Action(Card):
    _id = CardIds.ACTION
    _name = ""
    _description = "Gain 1 Action."


class Stunt(Card):
    _id = CardIds.STUNT
    _name = ""
    _description = "Gain 1 Stunt."


class Move(Card):
    _id = CardIds.MOVE
    _name = ""
    _description = "Move # of spaces up to your speed."


class React(Card):
    _id = CardIds.REACT
    _name = ""
    _description = "Gain 1 Reaction."


class DoubleMove(Card):
    _id = CardIds.DOUBLE_MOVE
    _name = ""
    _description = "Move # of spaces up to 2x your speed."


class Loot(Card):
    _id = CardIds.LOOT
    _name = ""
    _description = "Discard this card, draw 2 cards"


class Sprint(Card):
    _id = CardIds.SPRINT
    _name = ""
    _description = "Move # of spaces up to your speed, draw 1 card."


class SuperReact(Card):
    _id = CardIds.REACT
    _name = ""
    _description = "Gain 1 Reaction, draw 2 cards."


class ProficientDraw(Card):
    _id = CardIds.PROFICIENT_DRAW
    _name = ""
    _description = "Draw a # of cards = proficiency bonus."


class Boon(Card):
    _id = CardIds.BOON
    _name = ""
    _description = "Boon."


def get_card_from_id(_id: CardIds) -> Card:
    match _id:
        case CardIds.ACTION:
            return Action()
        case CardIds.STUNT:
            return Stunt()
        case CardIds.MOVE:
            return Move()
        case CardIds.REACT:
            return React()
        case CardIds.DOUBLE_MOVE:
            return DoubleMove()
        case CardIds.LOOT:
            return Loot()
        case CardIds.SPRINT:
            return Sprint()
        case CardIds.SUPER_REACT:
            return SuperReact()
        case CardIds.PROFICIENT_DRAW:
            return ProficientDraw()
        case CardIds.BOON:
            return Boon()
        case _:
            raise Exception(f"Could not find card for id {_id}")
