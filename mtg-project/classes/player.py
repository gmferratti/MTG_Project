from mtgsdk import Card
from classes.hand import Hand
from classes.library import Library
from classes.deck import Deck
from classes.graveyard import Graveyard
from classes.battlefield import Battlefield
import logging

logger = logging.getLogger(__name__)

class Player:
    """
    A class to represent a player in a Magic: The Gathering game.
    
    Attributes:
    -----------
    name : str
        The name of the player.
    deck : Deck or None
        The original deck used by the player, from which the library is created. It can be None.
    hand : Hand
        The hand of the player, representing the cards currently held.
    library : Library or None
        The library (deck) of the player, representing the remaining cards in the deck. It can be None.
    mulligan_count : int
        The number of mulligans the player has taken.
    turn : int
        The current turn number for the player.
    lands_played : int
        The number of lands played by the player in the current turn.
    extra_lands_allowed : int
        The extra number of lands a player can play per turn due to special effects.
    ready_to_play : bool
        Indicates if the player is ready to play (i.e., has a valid deck assigned).
    """

    def __init__(self, 
                 name: str = "Untitled Player", 
                 deck: Deck = None,
                 ):
        """
        Constructs all the necessary attributes for the Player object.
        
        Parameters:
        -----------
        name : str
            The name of the player.
        deck : Deck, optional
            The deck used by the player. It must be a valid deck if provided.
        """
        self.name = name
        self.deck = deck
        self.deck_name = deck.deck_name if deck else None

        self.hand = Hand()
        self.battlefield = Battlefield()
        self.library = Library(deck) if deck else None
        self.graveyard = Graveyard()

        self.mulligan_count = 0
        self.turn = 0  
        self.lands_played = 0
        self.spells_played = 0
        self.extra_lands = 0
        self.mana_pool = 0
        self.hand_size = 0

        self.valid_deck = deck.is_valid() if deck else False
        self.initial_hand_drawn = False 

    def play_a_match(self):
        return None

    def assign_deck(self, deck: Deck):
        """
        Assigns a deck to a player.
        
        Parameters:
        -----------
        deck : Deck
            The deck to be assigned to the player.
        
        Raises:
        -------
        ValueError:
            If the deck is not valid.
        """
        if not deck.is_valid():
            raise ValueError("The deck provided is not valid.")
        
        if self.deck is not None:
            raise RuntimeError("A deck has already been assigned to this player and cannot be reassigned.")

        self.deck = deck
        self.deck_name = deck.deck_name
        self.library = Library(deck)
        self.valid_deck = True

    def draw_initial_hand(self):
        """
        Draws the initial hand of 7 cards from the library and updates the library accordingly.
        Can only be called once directly; subsequent calls must be through the mulligan method.
        
        Raises:
        -------
        ValueError:
            If the player is not ready to play or if the initial hand has already been drawn.
        """
        if not self.valid_deck:
            raise ValueError("Player is not ready to play. Please assign a valid deck.")

        if self.initial_hand_drawn:
            raise ValueError("Initial hand has already been drawn. Use the mulligan method to draw a new hand.")

        self.library = Library(self.deck)
        self.library.shuffle()
        self.hand = Hand()
        
        for _ in range(7):
            drawn_card = self.library.draw_card()
            self.hand.add_card(drawn_card)

        self.hand_size = len(self.hand.cards)
        self.initial_hand_drawn = True
        self.hand.organize()


    def ask_mulligan(self):
        """
        Performs a mulligan if the player is ready to play, reducing the number of cards
        in the player's hand by one after drawing 7 cards.
        
        Raises:
        -------
        ValueError:
            If the player is not ready to play.
        """
        if not self.valid_deck:
            raise ValueError("Player is not ready to play. Please assign a valid deck.")
        
        if self.turn != 0:
            raise ValueError("Mulligan can only be performed at the beginning of the game.")

        self.mulligan_count += 1
        self.initial_hand_drawn = False
        self.draw_initial_hand()

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
        Advances the game to the next turn if the player is ready to play.
        
        Raises:
        -------
        ValueError:
            If the player is not ready to play.
        """
        if not self.valid_deck:
            raise ValueError("Player is not ready to play. Please assign a valid deck.")
        
        self.turn += 1
        self.lands_played = 0

        drawn_card = self.library.draw_card()
        self.hand.add_card(drawn_card)
        
        land_card = next((card for card in self.hand.cards if 'Land' in card.type), None)
        if land_card:
            self.play_land(land_card)

        self.play_spell(self.mana_pool)        

        if len(self.hand.cards) > 7:
            self.discard_card()
        
        self.hand.organize()

    def play_land(self, card: Card, extra_lands: int = 0) -> bool:
        """
        Attempts to play a land card if the player is ready to play.
        
        Parameters:
        -----------
        card : Card
            The land card to be played.
        extra_lands : int
            The number of extra lands the player is allowed to play this turn.
        
        Returns:
        --------
        bool
            True if the card was played, False otherwise.
        
        Raises:
        -------
        ValueError:
            If the player is not ready to play.
        """
        if not self.valid_deck:
            raise ValueError("Player is not ready to play. Please assign a valid deck.")

        self.extra_lands += extra_lands

        if 'Land' in card.type and self.lands_played < (1 + self.extra_lands):
            self.hand.remove_card(card)
            self.lands_played += 1

            self.battlefield.add_land(card)
            self.mana_pool = self.battlefield.calculate_mana_pool()
            
            logger.info(f"{self.name} played the land {card.name}.")
            
            return True
        else:
            logger.warning(f"{self.name} cannot play the land {card.name}.")
            return False
        
    def play_spell(self, available_mana: int) -> bool:
        """
        Attempts to play one or more spells if the player is ready to play.
        Optimizes mana usage by playing the best possible combination of spells.
        
        Parameters:
        -----------
        available_mana : int
            The amount of available mana for casting spells.
        
        Returns:
        --------
        bool
            True if some card was played, False otherwise.
        
        Raises:
        -------
        ValueError:
            If the player is not ready to play.
        """
        if not self.valid_deck:
            raise ValueError("Player is not ready to play. Please assign a valid deck.")

        # Ordena as cartas por custo de mana, do maior para o menor
        spells = [card for card in self.hand.cards if 'Land' not in card.type]
        spells.sort(key=lambda card: card.cmc, reverse=True)

        # Tenta jogar a melhor combinação de cartas
        mana_used = 0
        cards_to_play = []
        for spell in spells:
            if mana_used + spell.cmc <= available_mana:
                cards_to_play.append(spell)
                mana_used += spell.cmc

        if cards_to_play:
            for card in cards_to_play:
                self.hand.remove_card(card)
                self.spells_played += 1
                logger.info(f"{self.name} played the spell {card.name}.")
                self.graveyard.add_card(card)
            return True
        else:
            logger.warning(f"{self.name} couldn't play any spells.")
            return False

    def discard_card(self, return_to_library=False):
        """
        Discards a card from the player's hand. If `return_to_library` is True, the card is returned
        to the library (typically during a mulligan). Otherwise, the card is simply discarded, and 
        the number of not_played is incremented in the tracker.
        
        Parameters:
        -----------
        return_to_library : bool
            Whether the card should be returned to the library (e.g., during a mulligan).
        
        Raises:
        -------
        ValueError:
            If the player is not ready to play.
        """
        if not self.valid_deck:
            raise ValueError("Player is not ready to play. Please assign a valid deck.")
        
        # For simplicity, let's discard the card with the highest mana cost
        card_to_discard = max(self.hand.cards, key=lambda c: c.cmc)
        self.hand.remove_card(card_to_discard)
        
        if return_to_library:
            self.library.return_card(card_to_discard)
        else:
            self.graveyard.add_card(card_to_discard) 

    def __repr__(self):
        """
        Returns a string representation of the player in a more readable format.
        
        Returns:
        --------
        str
            A string representation showing the player's details over multiple lines.
        """
        library_size = len(self.library) if self.library else 0
        hand_size = len(self.hand) if self.hand else 0

        return (f"Player:\n"
                f"  Name: {self.name}\n"
                f"  Deck: {self.deck_name}\n"
                f"  Turn: {self.turn}\n"
                f"  Hand: {hand_size} cards\n"
                f"  Library: {library_size} cards\n"
                f"  Lands played: {self.lands_played}\n"
                f"  Mana pool: {self.mana_pool}\n"
                f"  Spells played: {self.spells_played}\n")
