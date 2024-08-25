from mtgsdk import Card

class Hand:
    """
    A class to represent a hand of cards for a player.
    
    Attributes:
    -----------
    cards : list of Card
        The cards currently in the player's hand.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the Hand object.
        """
        self.cards = []

    def add_card(self, card: Card):
        """
        Adds a card to the hand.
        
        Parameters:
        -----------
        card : Card
            The card to be added to the hand.
        """
        self.cards.append(card)

    def remove_card(self, card: Card):
        """
        Removes a card from the hand.
        
        Parameters:
        -----------
        card : Card
            The card to be removed from the hand.
        """
        self.cards.remove(card)

    def is_balanced(self) -> bool:
        """
        Checks if the hand has a balanced number of lands (2 to 4 lands).
        
        Returns:
        --------
        bool
            True if the hand has 2 to 4 lands, False otherwise.
        """
        land_count = sum(1 for card in self.cards if 'Land' in card.type)
        return 2 <= land_count <= 4

    def is_playable(self) -> bool:
        """
        Determines if the hand is playable in the early turns of the game.
        
        Returns:
        --------
        bool
            True if the hand has enough lands and a curve of spells that can be played
            in the first few turns, False otherwise.
        """
        land_count = sum(1 for card in self.cards if 'Land' in card.type)

        if land_count < 2:
            return False

        playable_spells = [
            card for card in self.cards
            if 'Land' not in card.type and card.cmc <= land_count
        ]

        return any(card.cmc <= 2 for card in playable_spells)

    def __len__(self):
        """
        Returns the number of cards in the hand.
        
        Returns:
        --------
        int
            The number of cards in the hand.
        """
        return len(self.cards)

    def __repr__(self):
        """
        Returns a string representation of the hand.
        
        Returns:
        --------
        str
            A string representation showing the cards in the hand.
        """
        return f"Hand({len(self.cards)} cards: {', '.join([card.name for card in self.cards])})"
