from mtgsdk import Card
from classes.plays import Plays
from classes.library import Library

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.player import Player

class Hand:
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

    def add_card(self, card: Card):
        """Adiciona uma carta à mão."""
        self.cards.append(card)

    def remove_card(self, card: Card):
        """Remove uma carta da mão."""
        self.cards.remove(card)

    def draw_cards(self, library: 'Library', num_cards: int = 7):
        """
        Draws a specified number of cards from the library into the hand.
        
        Parameters:
        -----------
        library : Library
            The library (deck) to draw cards from.
        num_cards : int
            The number of cards to draw. Defaults to 7.
        """
        for _ in range(min(num_cards, len(library))):
            self.add_card(library.draw_card())

    def play_land(self, card: Card, tracker: 'Plays', player: 'Player') -> bool:
        """
        Tenta jogar uma carta de terreno. Permite jogar mais de um terreno se
        o jogador tiver permissão extra. Registra o resultado no PlaysTracker.
        Retorna True se a carta foi jogada, False se não foi.
        """
        if 'Land' in card.type and player.lands_played < player.total_lands_allowed():
            self.remove_card(card)
            tracker.add_played()
            player.lands_played += 1
            return True
        else:
            tracker.add_not_played()
            return False

    def play_spell(self, tracker: 'Plays', available_mana: int) -> bool:
        """
        Tenta jogar uma ou mais mágicas (spells) otimizando o uso de mana.
        Verifica se há mana suficiente e tenta usar o máximo de mana possível.
        Registra o resultado no PlaysTracker.
        Retorna True se alguma carta foi jogada, False se nenhuma carta foi jogada.
        """
        # Ordena as cartas por custo de mana, do maior para o menor
        spells = [card for card in self.cards if 'Land' not in card.type]
        spells.sort(key=lambda card: card.cmc, reverse=True)
        
        # Tenta jogar a melhor combinação de cartas
        mana_used = 0
        cards_to_play = []
        for spell in spells:
            if mana_used + spell.cmc <= available_mana:
                cards_to_play.append(spell)
                mana_used += spell.cmc

        # Se alguma carta puder ser jogada
        if cards_to_play:
            for card in cards_to_play:
                self.remove_card(card)
                tracker.add_played()
            return True
        else:
            tracker.add_not_played()
            return False

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
