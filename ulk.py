import random

class CardDeck:
    def __init__(self, proficiency_bonus=4):
        self.proficiency_bonus = proficiency_bonus
        self.cards = [
            "Gain 1 Action", "Gain 1 Action", "Gain 1 Action", "Gain 1 Action",
            "Gain 1 Stunt.", "Gain 1 Stunt.", "Gain 1 Stunt.", "Gain 1 Stunt.",
            "Move # of spaces up to your speed.", "Move # of spaces up to your speed.",
            "Move # of spaces up to your speed.", "Move # of spaces up to your speed.",
            "Gain 1 Reaction.", "Gain 1 Reaction.", "Gain 1 Reaction.", "Gain 1 Reaction.",
            "Gain 1 Reaction.", "Gain 1 Reaction.", "Gain 1 Reaction.", "Gain 1 Reaction.",
            "Cast a Spell.", "Cast a Spell.", "Cast a Spell.", "Cast a Spell.",
            "Discard this card, draw 3 cards", "Discard this card, draw 3 cards",
            "Discard this card, draw 3 cards", "Discard this card, draw 3 cards",
            "Gain 2 Stunts, draw 1 card.", "Gain 2 Stunts, draw 1 card.",
            "Gain 2 Stunts, draw 1 card.", "Gain 2 Stunts, draw 1 card.",
            "Gain 1 Reaction, draw 1 card.", "Gain 1 Reaction, draw 1 card.",
            "Gain 1 Reaction, draw 1 card.", "Gain 1 Reaction, draw 1 card.",
            "Draw a # of cards = proficiency bonus.", "Draw a # of cards = proficiency bonus.",
            "Draw a # of cards = proficiency bonus.", "Draw a # of cards = proficiency bonus."
        ]
        self.discard_pile = []
        self.hand = []

    def shuffle_deck(self):
        self.cards += self.discard_pile
        self.discard_pile = []
        random.shuffle(self.cards)
        print("The deck has been shuffled.")

    def draw_cards(self, number, auto_process=True):
        for _ in range(number):
            if len(self.cards) == 0:
                print("No more cards in the deck to draw. Shuffling discard pile back into deck.")
                self.shuffle_deck()
                if len(self.cards) == 0:
                    print("No cards left to draw even after shuffling.")
                    return
            drawn_card = self.cards.pop()
            self.hand.append(drawn_card)
            print(f"Drew card: {drawn_card}")
        self.show_hand()
        if auto_process:
            self.auto_process_special_cards()

    def auto_process_special_cards(self):
        """
        Automatically scans your hand for any card that says:
          - "Discard this card, draw 3 cards" or 
          - "Draw a # of cards = proficiency bonus"
        When found, the card is removed (moved to the discard pile)
        and its effect is executed (drawing extra cards).
        """
        special_found = True
        while special_found:
            special_found = False
            i = 0
            while i < len(self.hand):
                card = self.hand[i]
                lower_card = card.lower()
                if "discard this card, draw 3 cards" in lower_card:
                    print(f"Auto-processing special card: {card}")
                    # Remove the special card from hand and add it to the discard pile
                    self.discard_pile.append(self.hand.pop(i))
                    # Draw 3 cards—but avoid triggering auto-processing in that call
                    self.draw_cards(3, auto_process=False)
                    special_found = True
                    # Break to re-scan the (updated) hand from the start
                    break
                elif "draw a # of cards" in lower_card and "proficiency bonus" in lower_card:
                    print(f"Auto-processing special card: {card}")
                    self.discard_pile.append(self.hand.pop(i))
                    self.draw_cards(self.proficiency_bonus, auto_process=False)
                    special_found = True
                    break
                else:
                    i += 1
            if special_found:
                self.show_hand()

    def discard_cards(self, indexes):
        indexes = sorted(indexes, reverse=True)
        for index in indexes:
            if 0 <= index < len(self.hand):
                self.discard_pile.append(self.hand.pop(index))
            else:
                print(f"Invalid index: {index}")
        print("Cards discarded.")
        self.show_hand()

    def return_all_cards(self):
        self.discard_pile += self.hand
        self.hand = []
        self.shuffle_deck()

    def show_hand(self):
        print("Current hand:")
        for i, card in enumerate(self.hand):
            print(f"{i}: {card}")

    def run(self):
        while True:
            print("\nOptions: draw <number>, discard <indexes>, return, shuffle, hand, quit")
            command = input("Enter command: ").strip().lower()
            if command.startswith("draw"):
                try:
                    number = int(command.split()[1])
                    self.draw_cards(number)
                except (IndexError, ValueError):
                    print("Please specify a valid number of cards to draw.")
            elif command.startswith("discard"):
                try:
                    indexes = list(map(int, command.split()[1:]))
                    self.discard_cards(indexes)
                except ValueError:
                    print("Please specify valid indexes to discard.")
            elif command == "return":
                self.return_all_cards()
            elif command == "shuffle":
                self.shuffle_deck()
            elif command == "hand":
                self.show_hand()
            elif command == "quit":
                print("Exiting the program.")
                break
            else:
                print("Invalid command. Please try again.")

if __name__ == "__main__":
    # Set your proficiency bonus here.
    deck = CardDeck(proficiency_bonus=4)
    deck.shuffle_deck()
    deck.run()
