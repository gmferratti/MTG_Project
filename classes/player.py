from classes.hand import Hand
from classes.library import Library
from classes.deck import Deck

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
    turno : int
        The current turn number for the player.
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
        drawn_card = self.library.draw_card()  # Retira uma carta da library
        self.hand.add_card(drawn_card)  # Adiciona a carta à mão
        
        # Verificar se a mão tem mais de 7 cartas e descartar uma se necessário
        if len(self.hand.cards) > 7:
            self.discard_card()

    def discard_card(self):
        """
        Discards a card from the player's hand if they have more than 7 cards.
        The discarded card is returned to the library.
        """
        # Por simplicidade, vamos descartar a carta com o maior custo de mana
        card_to_discard = max(self.hand.cards, key=lambda c: c.cmc)
        self.hand.remove_card(card_to_discard)
        self.library.return_card(card_to_discard)
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
