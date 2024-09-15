from mtgsdk import Card
from classes.hand import Hand
from classes.library import Library
from classes.deck import Deck
from classes.graveyard import Graveyard
from classes.battlefield import Battlefield
import random
import logging
import itertools

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
    spent_mana : int
        The amount of mana the player has spent in the current turn.
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
        self.match = 0
        self.spent_mana = 0

        self.valid_deck = deck.is_valid() if deck else False
        self.initial_hand_drawn = False 

        self.hand_mana_per_color = {'C': 0, 'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0}
        self.graveyard_mana_per_color = {'C': 0, 'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0}
        self.battlefield_mana_per_color = {'C': 0, 'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0}
        self.mana_pool_per_color = {'C': 0, 'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0}

    def play_a_match(self, 
                 tracker, 
                 max_mulligans, 
                 mulligan_prob, 
                 max_turns, 
                 hand_size_stop, 
                 extra_land_prob):
        """
        Simulates a Magic: The Gathering match for the player, including drawing an initial hand, performing mulligans,
        playing lands (including extra lands if allowed), and taking turns up to the maximum specified.

        Parameters:
        -----------
        tracker : PlayerTracker
            Object that tracks and logs the player's state at the end of each turn.
        max_mulligans : int
            Maximum number of mulligans allowed for the player in this match.
        mulligan_prob : float
            Probability (between 0 and 1) that the player will choose to mulligan after drawing an initial hand.
        max_turns : int
            Maximum number of turns allowed for the match.
        hand_size_stop : int
            Minimum hand size threshold. The simulation will stop if the player's hand size reaches this value.
        extra_land_prob : float
            Probability (between 0 and 1) that the player will play an additional land during each turn.

        Returns:
        --------
        None
        """
        # Increment the match count
        self.match += 1
        logger.info(f"Starting match {self.match} for player {self.name}")
        
        # Draw initial hand
        self.draw_initial_hand()
        tracker.log_turn(self)  # Log initial state
        
        # Mulligan simulation
        mulligan_count = 0
        while mulligan_count < max_mulligans:
            if random.random() < mulligan_prob:
                logger.info(f"Player '{self.name}' is taking a mulligan in match {self.match}.")
                self.ask_mulligan()
                mulligan_count += 1
                tracker.log_turn(self)  # Log state after mulligan
            else:
                logger.info(f"Player '{self.name}' kept their hand in match {self.match}.")
                break
        
        # Turn simulation with extra land plays
        for turn in range(1, max_turns + 1):
            self.next_turn()

            # Stop if hand size reaches hand_size_stop
            if len(self.hand.cards) <= hand_size_stop:
                logger.info(f"Player '{self.name}' has reached hand_size_stop with {len(self.hand.cards)} cards in match {self.match}. Stopping simulation.")
                break

            # Extra land play
            if random.random() < extra_land_prob:
                self.extra_lands += 1
                logger.info(f"Player '{self.name}' plays an extra land in match {self.match}. Total extra lands this turn: {self.extra_lands}")
                
                land_cards = [card for card in self.hand.cards if 'Land' in card.type]
                if land_cards: 
                    self.play_land(land_cards[0])
                    self.mana_pool = self.battlefield.calculate_mana_pool()
                    self.mana_pool_per_color = self.battlefield.calculate_mana_pool_per_color()
                else:
                    logger.info(f"Player '{self.name}' has no land cards to play as extra land in match {self.match}.")

                # Reset extra_lands after playing
                self.extra_lands = 0

            tracker.log_turn(self)  # Log the state at the end of each turn
        
        # End the match
        logger.info(f"Match {self.match} for player {self.name} completed.")
        self.new_match()


    def new_match(self):
        """
        Resets the player's attributes at the end of a match.
        """
        self.hand = Hand()
        self.battlefield = Battlefield()
        self.library = Library(self.deck)
        self.graveyard = Graveyard()
        self.mulligan_count = 0
        self.turn = 0  
        self.lands_played = 0
        self.spells_played = 0
        self.extra_lands = 0
        self.mana_pool = 0
        self.hand_size = 0
        self.initial_hand_drawn = False
        self.hand_mana_per_color = {'C': 0, 'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0}
        self.graveyard_mana_per_color = {'C': 0, 'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0}
        self.battlefield_mana_per_color = {'C': 0, 'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0}
        self.mana_pool_per_color = {'C': 0, 'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0}

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

    def mana_colors_in_hand(self):
        """
        Calculates the amount of mana of each color in the player's hand, including
        mana from non-spell cards such as lands (which are based on color identity).
        """
        # Reset the mana counts
        self.hand_mana_per_color = {'C': 0, 'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0}
        
        for card in self.hand.cards:
            # Check if the card has a mana cost
            if card.mana_cost:
                symbols = card.mana_cost.replace("{", "").replace("}", "").split()
                for symbol in symbols:
                    if symbol in self.hand_mana_per_color:
                        self.hand_mana_per_color[symbol] += 1
                    elif symbol.isdigit():
                        self.hand_mana_per_color['C'] += int(symbol)
            
            # If no mana cost (likely a land), check color identity
            elif card.color_identity:
                for color in card.color_identity:
                    if color in self.hand_mana_per_color:
                        self.hand_mana_per_color[color] += 1
        
        return self.hand_mana_per_color


    def mana_colors_in_graveyard(self):
        """
        Calculates the amount of mana of each color in the player's graveyard.
        """
        # Reset the mana counts
        self.graveyard_mana = {'C': 0, 'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0}
        
        for card in self.graveyard.cards:
            if card.mana_cost:
                for symbol in card.mana_cost:
                    if symbol in self.graveyard_mana:
                        self.graveyard_mana[symbol] += 1
                    elif symbol.isdigit():
                        self.graveyard_mana['C'] += int(symbol)

        return self.graveyard_mana

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
        self.spent_mana = 0 
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

        
    def play_land(self, land_card: Card) -> bool:
        """
        Attempts to play a land card if the player is ready to play.
        Prioritizes playing a land that produces mana of the color with the highest affinity in the player's hand.

        Parameters:
        -----------
        land_card : Card
            The land card to be played.

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

        if self.lands_played >= (1 + self.extra_lands):
            logger.warning(f"{self.name} cannot play any more lands this turn.")
            return False

        # Calcula a afinidade de cores na mão
        color_affinity = {'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0}
        for card in self.hand.cards:
            if card.mana_cost:
                for symbol in card.mana_cost:
                    if symbol in color_affinity:
                        color_affinity[symbol] += 1

        # Identifica a cor com maior afinidade
        dominant_color = max(color_affinity, key=color_affinity.get)
        logger.info(f"{self.name} has a dominant color affinity for: {dominant_color}")

        # Filtra os terrenos na mão
        land_cards = [card for card in self.hand.cards if 'Land' in card.type]

        if not land_cards:
            logger.warning(f"{self.name} has no land cards to play.")
            return False

        # Encontra o terreno que mais se alinha com a cor dominante
        preferred_land = None
        for land in land_cards:
            # Se o terreno puder produzir mana da cor dominante
            if land.color_identity and dominant_color in land.color_identity:
                preferred_land = land
                break

        # Se nenhum terreno da cor dominante for encontrado, joga qualquer terreno disponível
        if not preferred_land:
            # Caso não tenha terrenos com afinidade dominante, joga o terreno passado como argumento
            preferred_land = land_card  # Usa o terreno passado como argumento

        # Joga o terreno
        self.hand.remove_card(preferred_land)
        self.lands_played += 1
        self.battlefield.add_land(preferred_land)

        # Atualiza o pool de mana com base no terreno jogado
        if preferred_land.color_identity:
            for color in preferred_land.color_identity:
                if color in self.mana_pool_per_color:
                    self.mana_pool_per_color[color] += 1

        # Atualiza o pool de mana cumulativo
        self.mana_pool = self.battlefield.calculate_mana_pool()
        self.mana_pool_per_color = self.battlefield.calculate_mana_pool_per_color()

        logger.info(f"{self.name} played the land {preferred_land.name} to support the color {dominant_color}.")
        logger.info(f"Current mana pool: {self.mana_pool_per_color}")

        return True


    def play_spell(self, available_mana: int) -> bool:
        """
        Attempts to play the combination of spells that maximizes the total mana spent, 
        while ensuring the player has enough mana of each color to cast them.

        Parameters:
        -----------
        available_mana : int
            The total available mana for casting spells.

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
        
        # Lista de todas as magias na mão
        spells = [card for card in self.hand.cards if 'Land' not in card.type]
        
        # Verifica todas as combinações possíveis de magias (subconjuntos)
        max_mana_spent = 0
        best_combo = []

        for num_cards in range(1, len(spells) + 1):
            for combo in itertools.combinations(spells, num_cards):
                mana_required_total = {'C': 0, 'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0}
                mana_spent = 0
                can_cast_combo = True

                # Calcula o mana necessário para lançar essa combinação de cartas
                for spell in combo:
                    mana_required = {'C': 0, 'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0}
                    
                    if spell.mana_cost:
                        for symbol in spell.mana_cost:
                            if symbol in mana_required:
                                mana_required[symbol] += 1
                            elif symbol.isdigit():  # Mana incolor ou genérica
                                mana_required['C'] += int(symbol)
                    
                    # Adiciona o mana requerido para o total
                    for color in mana_required:
                        mana_required_total[color] += mana_required[color]
                    
                    mana_spent += spell.cmc
                
                # Verifica se há mana suficiente para lançar essa combinação de cartas
                for color, required in mana_required_total.items():
                    if required > self.mana_pool_per_color[color]:
                        can_cast_combo = False
                        break
                
                # Se essa combinação é válida e usa mais mana do que a combinação atual, atualiza a melhor
                if can_cast_combo and mana_spent > max_mana_spent:
                    max_mana_spent = mana_spent
                    best_combo = combo

        # Joga a melhor combinação de cartas, se possível
        if best_combo:
            for card in best_combo:
                # Calcula o mana necessário para essa carta
                mana_required = {'C': 0, 'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0}
                if card.mana_cost:
                    for symbol in card.mana_cost:
                        if symbol in mana_required:
                            mana_required[symbol] += 1
                        elif symbol.isdigit():  # Mana incolor ou genérica
                            mana_required['C'] += int(symbol)

                # Deduz o mana do pool de mana
                for color, used in mana_required.items():
                    self.mana_pool_per_color[color] -= used

                # Joga a carta
                self.hand.remove_card(card)
                self.spells_played += 1
                self.spent_mana += card.cmc
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
