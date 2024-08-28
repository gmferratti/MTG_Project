from mtgsdk import Card
from classes.library import Library

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.player import Player

class Hand():
    """
    A class to represent a hand of cards for a player.
    
    Attributes:
    -----------
    cards : list of Card
        The cards currently in the player's hand.
    """

    MAX_HAND_SIZE = 7
    MAX_LANDS_PER_TURN = 1

    def __init__(self):
        self.cards = []
        self.hand_size = 0

    def add_card(self, card: Card):
        """Adiciona uma carta específica à mão."""
        self.cards.append(card)

    def remove_card(self, card: Card):
        """Remove uma carta específica da mão."""
        self.cards.remove(card)

    def draw(self, library: 'Library', num_cards: int = 1):
        """
        Draws a specified number of cards from the library into the hand.
        
        Parameters:
        -----------
        library : Library
            The library (deck) to draw cards from.
        num_cards : int
            The number of cards to draw. Defaults to 1.
        """
        for _ in range(min(num_cards, len(library))):
            drawn_card = library.draw_card()
            self.cards.append(drawn_card)
    
    def organize(self):
        """
        Organizes the hand by placing land cards at the beginning of the list
        and other cards at the end.
        """
        lands = [card for card in self.cards if 'Land' in card.type]
        non_lands = [card for card in self.cards if 'Land' not in card.type]
        self.cards = lands + non_lands

    def is_above_hand_limit(self) -> bool:
        """Verifica se o número de cartas na mão está acima do limite permitido."""
        return len(self.cards) > self.MAX_HAND_SIZE
    
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
        """Retorna o número de cartas na mão."""
        return len(self.cards)

    def __repr__(self):
        """Retorna uma representação em string da mão."""
        return f"Hand({len(self.cards)} cards: {', '.join([card.name for card in self.cards])})"
