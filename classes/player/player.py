from hand import Hand
from deck import Deck
from library import Library

class Player:
    """
    A class to represent a player in a Magic: The Gathering game.
    
    Attributes:
    -----------
    name : str
        The name of the player.
    deck : Deck
        The original deck used by the player, from which the library is created.
    hand : Hand
        The hand of the player, representing the cards currently held.
    library : Library
        The library (deck) of the player, representing the remaining cards in the deck.
    mulligan_count : int
        The number of mulligans the player has taken.
    """

    def __init__(self, name: str, deck: Deck):
        """
        Constructs all the necessary attributes for the Player object.
        
        Parameters:
        -----------
        name : str
            The name of the player.
        deck : Deck
            The deck used by the player. It must be a valid deck.
        
        Raises:
        -------
        ValueError:
            If the deck is not valid.
        """
        if not deck.is_valid():
            raise ValueError("The deck provided is not valid.")
        
        self.name = name
        self.deck = deck
        self.mulligan_count = 0
        self.hand = Hand()
        self.library = Library(deck)


    def draw_initial_hand(self):
        """
        Draws the initial hand of 7 cards from the library.
        """
        self.hand = Hand()
        for _ in range(7):
            self.hand.add_card(self.library.draw_card())

    def mulligan(self):
        """
        Performs a mulligan, reducing the number of cards in the player's hand by one
        after drawing 7 cards. Cards are returned to the library based on balance rules.
        """
        self.mulligan_count += 1
        self.draw_initial_hand()

        cards_to_return = self.mulligan_count

        while cards_to_return > 0 and len(self.hand.cards) > 0:
            land_cards = [card for card in self.hand.cards if 'Land' in card.type]
            
            if len(land_cards) > 0 and not self.hand.is_balanced() and len(land_cards) > 2:
                card_to_return = land_cards.pop()
            else:
                card_to_return = max(self.hand.cards, key=lambda c: c.cmc)

            self.hand.remove_card(card_to_return)
            self.library.return_card(card_to_return)
            cards_to_return -= 1

    def __repr__(self):
        """
        Returns a string representation of the player.
        
        Returns:
        --------
        str
            A string representation showing the player's name, hand, and library.
        """
        return f"Player({self.name}, Hand: {self.hand}, Library: {self.library})"
