import random

class Hand:
    """
    A class to represent a hand of cards for a player.
    
    Attributes:
    -----------
    cards : list of Card
        The cards currently in the player's hand.
    """

    def __init__(self, deck):
        """
        Constructs all the necessary attributes for the Hand object.
        
        Parameters:
        -----------
        deck : Deck
            The deck from which cards will be drawn. It must be a valid deck.
        """
        self.cards = []
        self.deck = deck

    def draw_cards(self, number_of_cards=7):
        """
        Draws a specified number of cards from the deck.
        
        Parameters:
        -----------
        number_of_cards : int, optional
            The number of cards to draw from the deck (default is 7).
            
        Raises:
        -------
        ValueError:
            If the deck has fewer cards than the number of cards to draw.
        """
        if len(self.deck.cards) < number_of_cards:
            raise ValueError("Not enough cards in the deck to draw the specified number.")
        
        # Embaralhar a mão de volta no deck antes de fazer o mulligan
        self.deck.cards.extend(self.cards)
        random.shuffle(self.deck.cards)
        
        # Sortear as novas cartas
        self.cards = random.sample(self.deck.cards, number_of_cards)
        
        # Remover as cartas sorteadas do deck
        for card in self.cards:
            self.deck.cards.remove(card)

    def __repr__(self):
        """
        Returns a string representation of the hand.
        
        Returns:
        --------
        str
            A string representation showing the cards in the hand.
        """
        return f"Hand({len(self.cards)} cards: {', '.join([card.name for card in self.cards])})"