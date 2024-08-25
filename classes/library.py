from mtgsdk import Card
from classes.deck import Deck

class Library:
    """
    A class to represent the library (deck) of a player in a Magic: The Gathering game.
    
    Attributes:
    -----------
    cards : list of Card
        The cards currently in the library (deck).
    """

    def __init__(self, deck: Deck):
        """
        Constructs all the necessary attributes for the Library object.
        
        Parameters:
        -----------
        deck : Deck
            The deck from which the library will be constructed. It must be a valid deck.
        """
        if not deck.is_valid():
            raise ValueError("The deck provided is not valid.")
        
        self.cards = deck.cards[:]  # Copia as cartas do deck para a library

    def draw_card(self):
        """
        Draws a single card from the library.
        
        Returns:
        --------
        Card
            The card drawn from the library.
        """
        if len(self.cards) == 0:
            raise ValueError("Cannot draw from an empty library.")
        
        return self.cards.pop(0)  # Retira a primeira carta do deck

    def return_card(self, card: Card):
        """
        Returns a card to the library.
        
        Parameters:
        -----------
        card : Card
            The card to be returned to the library.
        """
        self.cards.append(card)

    def shuffle(self):
        """
        Shuffles the library.
        """
        import random
        random.shuffle(self.cards)

    def __len__(self):
        """
        Returns the number of cards in the library.
        
        Returns:
        --------
        int
            The number of cards in the library.
        """
        return len(self.cards)

    def __repr__(self):
        """
        Returns a string representation of the library.
        
        Returns:
        --------
        str
            A string representation showing the number of cards in the library.
        """
        return f"Library({len(self.cards)} cards)"
