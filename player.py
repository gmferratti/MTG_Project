from hand import Hand

class Player:
    """
    A class to represent a player in a Magic: The Gathering game.
    
    Attributes:
    -----------
    name : str
        The name of the player.
    hand : Hand
        The hand of the player, represented by the Hand subclass.
    deck : Deck
        The deck used by the player.
    mulligan_count : int
        The number of mulligans the player has taken.
    """

    def __init__(self, name, deck):
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
        self.hand = Hand(deck)

    def mulligan(self):
        """
        Performs a mulligan, reducing the number of cards in the player's hand by one, down to a minimum of zero.
        """
        self.mulligan_count += 1
        cards_to_draw = max(7 - self.mulligan_count, 0)
        self.hand.draw_cards(cards_to_draw)
