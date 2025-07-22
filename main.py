import games
import piles
from cards import CardIds

CARD_COUNTS = {
    CardIds.ACTION: 4,
    CardIds.STUNT: 4,
    CardIds.MOVE: 4,
    CardIds.REACT: 8,
    CardIds.DOUBLE_MOVE: 4,
    CardIds.LOOT: 4,
    CardIds.SPRINT: 4,
    CardIds.SUPER_REACT: 4,
    CardIds.PROFICIENT_DRAW: 4,
    CardIds.BOON: 2,
}


def main():
    deck = build_deck()
    game_state = games.GameState(deck=deck, proficiency_bonus=4, verbosity_level=1)
    game_state.shuffle_deck()
    run(game_state)


def build_deck() -> piles.Pile:
    deck_card_ids = []
    for card_id, num_copies in CARD_COUNTS.items():
        for _ in range(num_copies):
            deck_card_ids.append(card_id)
    return piles.get_pile_from_ids(deck_card_ids)


def run(game_state):
    while True:
        command = _prompt_for_command()
        try:
            _process_command(command, game_state)
        except UserRequestedQuit:
            print("Exiting the program.")
            return
        except InvalidCommand:
            print("Invalid command. Please try again.")
        print("~" * 50)


def _prompt_for_command() -> str:
    print("\nOptions: draw <number>, discard <indexes>, return, shuffle, hand, quit")
    return input("Enter command: ").strip().lower()


def _process_command(command: str, game_state: games.GameState) -> None:
    if command.startswith("draw"):
        _draw(command, game_state)
    elif command.startswith("discard"):
        _discard(command, game_state)
    elif command == "return":
        game_state.return_all_cards()
    elif command == "shuffle":
        game_state.shuffle_deck()
    elif command == "hand":
        _show_hand(game_state)
    elif command == "quit":
        raise UserRequestedQuit()
    else:
        raise InvalidCommand()


def _draw(command, gamestate):
    try:
        number = int(command.split()[1])
        gamestate.draw_cards(number)
    except (IndexError, ValueError):
        print("Please specify a valid number of cards to draw.")


def _discard(command, gamestate):
    try:
        indices = list(map(int, command.split()[1:]))
        gamestate.discard_multiple(indices)
    except ValueError:
        print("Please specify valid indexes to discard.")


def _show_hand(game_state: games.GameState):
    print(game_state.get_hand_str())


class UserRequestedQuit(Exception):
    pass


class InvalidCommand(Exception):
    pass


if __name__ == "__main__":
    main()
