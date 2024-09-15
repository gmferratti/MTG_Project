from mtgsdk import Card
import logging

logger = logging.getLogger(__name__)

class Graveyard:
    """
    A class to represent the graveyard in a Magic: The Gathering game.

    This class serves as a simple container for cards that have been used, 
    destroyed, or discarded. Once a card enters the graveyard, it stays there.
    
    Attributes:
    -----------
    cards : list of Card
        The cards currently in the graveyard.
    """

    def __init__(self):
        self.cards = []

    def add_card(self, card: Card):
        """
        Adds a card to the graveyard.

        Parameters:
        -----------
        card : Card
            The card to be added to the graveyard.
        """
        logger.info(f"{card.name} added to the graveyard.")
        self.cards.append(card)

    def __len__(self):
        """
        Returns the number of cards in the graveyard.

        Returns:
        --------
        int
            The number of cards in the graveyard.
        """
        return len(self.cards)

    def __repr__(self):
        """
        Returns a string representation of the graveyard.

        Returns:
        --------
        str
            A string representation of the cards in the graveyard.
        """
        max_display = 5

        if len(self.cards) > max_display:
            displayed_cards = ', '.join(card.name for card in self.cards[:max_display])
            return (f"Graveyard({len(self.cards)} cards: {displayed_cards}, ... "
                    f"+ {len(self.cards) - max_display} more)")
        else:
            displayed_cards = ', '.join(card.name for card in self.cards)
            return f"Graveyard({len(self.cards)} cards: {displayed_cards})"
        
    def mana_colors_in_graveyard(self):
        """
        Calculates the amount of mana of each color in the player's graveyard.
        """
        # Reset the mana counts
        self.graveyard_mana_per_color = {'C': 0, 'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0}
        
        for card in self.graveyard.cards:
            if card.mana_cost:
                symbols = card.mana_cost.replace("{", "").replace("}", " ").split()
                for symbol in symbols:
                    if symbol in self.graveyard_mana_per_color:
                        self.graveyard_mana_per_color[symbol] += 1
                    elif symbol.isdigit():  # Contabilizar mana genérica/incolor
                        self.graveyard_mana_per_color['C'] += int(symbol)

        return self.graveyard_mana_per_color

