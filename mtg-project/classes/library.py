import random
from mtgsdk import Card
from classes.deck import Deck
import logging

logger = logging.getLogger(__name__)

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
        
        self.cards = deck.cards[:]
        self.library_size = len(self.cards)

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
        
        popped_card = self.cards.pop(0)
        self.library_size = len(self.cards)

        return popped_card

    def return_card(self, card: Card):
        """
        Returns a card to the library.
        
        Parameters:
        -----------
        card : Card
            The card to be returned to the library.
        """
        logger.info("Returning {} to the library after mulligan".format(card.name))
        self.cards.append(card)
        self.shuffle()
        self.library_size = len(self.cards)

    def shuffle(self):
        """
        Shuffles the library.
        """
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
