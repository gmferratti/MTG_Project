import pandas as pd
from classes.player import Player

class PlayerTracker:
    """
    A class to track and record the player's attributes during each turn.
    """
    def __init__(self):
        # Inicializa um DataFrame vazio com as colunas correspondentes aos atributos do Player
        self.data = pd.DataFrame(columns=[
            'name', 'deck_name', 'deck_colors', 'turn', 'mulligan_count', 'lands_played',
            'spells_played', 'extra_lands', 'mana_pool', 'hand_size', 'deck_size',
            'graveyard_size', 'full_hand', 'full_graveyard'
        ])

    def log_turn(self, player):
        """
        Logs the current state of the player at the end of a turn into the DataFrame.

        Args:
            player (Player): The player whose state is being logged.
        """
        # Cria um dicionário com os atributos do player
        player_data = {
            'name': player.name,
            'deck_name': player.deck_name,
            'deck_colors': player.deck.deck_colors,
            'turn': player.turn,
            'mulligan_count': player.mulligan_count,
            'lands_played': player.lands_played,
            'spells_played': player.spells_played,
            'extra_lands': player.extra_lands,
            'mana_pool': player.mana_pool,
            'hand_size': len(player.hand.cards),
            'deck_size': len(player.deck.cards),
            'graveyard_size': len(player.graveyard),
            'full_hand': repr(player.hand),
            'full_graveyard': repr(player.graveyard)
        }
        
        # Cria um DataFrame temporário para adicionar a nova linha
        new_row = pd.DataFrame([player_data])
        
        # Usa pd.concat para adicionar a nova linha ao DataFrame existente
        self.data = pd.concat([self.data, new_row], ignore_index=True)    
    
    def get_data(self):
        """
        Returns the DataFrame containing the logged player data.
        """
        return self.data
