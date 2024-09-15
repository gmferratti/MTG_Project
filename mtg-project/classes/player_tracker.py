import pandas as pd
from classes.player import Player

class PlayerTracker:
    """
    A class to track and record the player's attributes during each turn.
    """
    def __init__(self):
        # Inicializa um DataFrame vazio com as colunas correspondentes aos atributos do Player
        self.data = pd.DataFrame(columns=[
            'name', 'deck_name', 'deck_colors', 'match', 'turn', 'mulligan_count', 'lands_played',
            'spells_played', 'mana_pool', 'spent_mana', 'hand_size', 'library_size',
            'graveyard_size', 'full_hand', 'full_graveyard', 
            'hand_W', 'hand_U', 'hand_B', 'hand_R', 'hand_G', 'hand_C',
            'graveyard_W', 'graveyard_U', 'graveyard_B', 'graveyard_R', 'graveyard_G', 'graveyard_C',
            'mana_pool_W', 'mana_pool_U', 'mana_pool_B', 'mana_pool_R', 'mana_pool_G', 'mana_pool_C',
            'battlefield_W', 'battlefield_U', 'battlefield_B', 'battlefield_R', 'battlefield_G', 'battlefield_C'
        ])

    def log_turn(self, player):
        """
        Logs the current state of the player at the end of a turn into the DataFrame.

        Args:
            player (Player): The player whose state is being logged.
        """
        # Cria um dicionário com os atributos do player, incluindo o mana por cor
        player_data = {
            'name': player.name,
            'deck_name': player.deck_name,
            'deck_colors': player.deck.deck_colors,
            'match': player.match,
            'turn': player.turn,
            'mulligan_count': player.mulligan_count,
            'lands_played': player.lands_played,
            'spells_played': player.spells_played,
            'mana_pool': player.mana_pool,
            'spent_mana': player.spent_mana,
            'hand_size': len(player.hand.cards),
            'library_size': len(player.library),
            'graveyard_size': len(player.graveyard),
            'full_hand': repr(player.hand),
            'full_graveyard': repr(player.graveyard),
            'hand_W': player.hand_mana_per_color['W'],
            'hand_U': player.hand_mana_per_color['U'],
            'hand_B': player.hand_mana_per_color['B'],
            'hand_R': player.hand_mana_per_color['R'],
            'hand_G': player.hand_mana_per_color['G'],
            'hand_C': player.hand_mana_per_color['C'],
            'graveyard_W': player.graveyard_mana_per_color['W'],
            'graveyard_U': player.graveyard_mana_per_color['U'],
            'graveyard_B': player.graveyard_mana_per_color['B'],
            'graveyard_R': player.graveyard_mana_per_color['R'],
            'graveyard_G': player.graveyard_mana_per_color['G'],
            'graveyard_C': player.graveyard_mana_per_color['C'],
            'mana_pool_W': player.mana_pool_per_color['W'],
            'mana_pool_U': player.mana_pool_per_color['U'],
            'mana_pool_B': player.mana_pool_per_color['B'],
            'mana_pool_R': player.mana_pool_per_color['R'],
            'mana_pool_G': player.mana_pool_per_color['G'],
            'mana_pool_C': player.mana_pool_per_color['C'],
            'battlefield_W': player.battlefield_mana_per_color['W'],
            'battlefield_U': player.battlefield_mana_per_color['U'],
            'battlefield_B': player.battlefield_mana_per_color['B'],
            'battlefield_R': player.battlefield_mana_per_color['R'],
            'battlefield_G': player.battlefield_mana_per_color['G'],
            'battlefield_C': player.battlefield_mana_per_color['C']
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
