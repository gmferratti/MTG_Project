from mtgsdk import Card
from classes.hand import Hand
from classes.library import Library
from classes.deck import Deck
from classes.plays import Plays

class Player:
    """
    A class to represent a player in a Magic: The Gathering game.
    
    Attributes:
    -----------
    name : str
        The name of the player.
    deck : Deck
        The original deck used by the player, from which the library is created.
    hand : Hand
        The hand of the player, representing the cards currently held.
    library : Library
        The library (deck) of the player, representing the remaining cards in the deck.
    mulligan_count : int
        The number of mulligans the player has taken.
    turn : int
        The current turn number for the player.
    lands_played : int
        The number of lands played by the player in the current turn.
    extra_lands_allowed : int
        The extra number of lands a player can play per turn due to special effects.
    """

    def __init__(self, name: str, deck: Deck):
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
        self.deck = deck  # Armazena o deck original
        self.mulligan_count = 0
        self.turn = 0  # Inicializa o turno como 0
        self.lands_played = 0  # Inicializa os terrenos jogados no turno como 0
        self.extra_lands_allowed = 0  # Inicializa os terrenos extras permitidos como 0
        self.hand = Hand()  # A mão é criada vazia
        self.library = Library(deck)  # A biblioteca é criada a partir do deck

    def draw_initial_hand(self):
        """
        Draws the initial hand of 7 cards from the library.
        """
        self.hand = Hand()  # Reseta a mão
        for _ in range(7):
            self.hand.add_card(self.library.draw_card())

    def mulligan(self):
        """
        Performs a mulligan, reducing the number of cards in the player's hand by one
        after drawing 7 cards. Cards are returned to the library based on balance rules.
        """
        self.mulligan_count += 1
        self.draw_initial_hand()  # Compra sempre 7 cartas

        cards_to_return = self.mulligan_count

        while cards_to_return > 0 and len(self.hand.cards) > 0:
            land_cards = [card for card in self.hand.cards if 'Land' in card.type]
            
            if len(land_cards) > 0 and not self.hand.is_balanced() and len(land_cards) > 2:
                card_to_return = land_cards.pop()
            else:
                card_to_return = max(self.hand.cards, key=lambda c: c.cmc)

            self.hand.remove_card(card_to_return)
            self.library.return_card(card_to_return)
            cards_to_return -= 1

    def next_turn(self):
        """
        Advances the game to the next turn. The player draws one card from the library
        and adds it to their hand. If the player has more than 7 cards in hand at the
        end of the turn, they must discard a card. The turn number is incremented.
        """
        self.turn += 1  # Incrementa o turno
        self.lands_played = 0  # Reseta os terrenos jogados no turno
        drawn_card = self.library.draw_card()  # Retira uma carta da library
        self.hand.add_card(drawn_card)  # Adiciona a carta à mão
        
        # Verificar se a mão tem mais de 7 cartas e descartar uma se necessário
        if len(self.hand.cards) > 7:
            self.discard_card()

    def allow_extra_land(self, extra_lands: int):
        """
        Permite que o jogador jogue terrenos extras neste turno.
        
        Parameters:
        -----------
        extra_lands : int
            The number of extra lands the player is allowed to play this turn.
        """
        self.extra_lands_allowed += extra_lands

    def total_lands_allowed(self) -> int:
        """
        Retorna o número total de terrenos que o jogador pode jogar no turno atual,
        incluindo terrenos extras permitidos.
        """
        return 1 + self.extra_lands_allowed

    def play_land(self, card: Card, tracker: 'Plays') -> bool:
        """
        Tenta jogar uma carta de terreno. Permite jogar mais de um terreno se
        o jogador tiver permissão extra. Registra o resultado no PlaysTracker.
        Retorna True se a carta foi jogada, False se não foi.
        """
        if self.lands_played < (1 + self.extra_lands_allowed):
            if self.hand.play_land(card, tracker, self):
                print(f"{self.name} jogou o terreno {card.name}.")
                return True
        print(f"{self.name} não pode jogar o terreno {card.name}.")
        return False

    def play_spell(self, tracker: 'Plays', available_mana: int) -> bool:
        """
        Tenta jogar uma ou mais mágicas (spells) otimizando o uso de mana.
        Verifica se há mana suficiente e tenta usar o máximo de mana possível.
        Registra o resultado no PlaysTracker.
        Retorna True se alguma carta foi jogada, False se nenhuma carta foi jogada.
        """
        if self.hand.play_spell(tracker, available_mana):
            print(f"{self.name} jogou uma ou mais mágicas usando {available_mana} mana.")
            return True
        print(f"{self.name} não conseguiu jogar nenhuma mágica.")
        return False

    def discard_card(self, tracker: 'Plays', return_to_library=False):
        """
        Discards a card from the player's hand. If `return_to_library` is True, the card is returned
        to the library (typically during a mulligan). Otherwise, the card is simply discarded, and 
        the number of not_played is incremented in the tracker.
        
        Parameters:
        -----------
        tracker : Plays
            The tracker that records the number of successful and unsuccessful plays.
        return_to_library : bool
            Whether the card should be returned to the library (e.g., during a mulligan).
        """
        # Por simplicidade, vamos descartar a carta com o maior custo de mana
        card_to_discard = max(self.hand.cards, key=lambda c: c.cmc)
        self.hand.remove_card(card_to_discard)
        
        if return_to_library:
            self.library.return_card(card_to_discard)
            print(f"{self.name} retorna {card_to_discard.name} para a library.")
        else:
            tracker.add_not_played()
            print(f"{self.name} descarta {card_to_discard.name}.")

    def __repr__(self):
        """
        Returns a string representation of the player.
        
        Returns:
        --------
        str
            A string representation showing the player's name, hand, library, and current turn.
        """
        return f"Player({self.name}, Turn: {self.turn}, Hand: {self.hand}, Library: {self.library})"