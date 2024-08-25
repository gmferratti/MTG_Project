import pandas as pd
from typing import Dict, Union
from mtgsdk import Card


class Deck:
    """
    A class to represent a deck of Magic: The Gathering cards.
    """

    def __init__(self, allowed_sets=None, allowed_colors=None, min_cards=60, max_cards=80, min_lands=18, max_lands=30, language="EN", max_cards_per_deck=4, exception_cards=None):
        """
        Constructs all the necessary attributes for the Deck object.
        """
        self.allowed_sets = allowed_sets
        self.allowed_colors = allowed_colors
        self.min_cards = min_cards
        self.max_cards = max_cards
        self.min_lands = min_lands
        self.max_lands = max_lands
        self.language = language
        self.max_cards_per_deck = max_cards_per_deck
        self.exception_cards = exception_cards or []

        self.cards = []
        self.deck_name = None  # Atributo para armazenar o nome do deck

    def load_deck_from_txt(self, file_path: str):
        """
        Loads the deck name and cards from a .txt file and assigns them to the Deck object.

        Args:
            file_path (str): The path to the .txt file containing the deck information.

        Returns:
            None
        """
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Extrair o nome do deck
        deck_list_started = False
        for line in lines:
            line = line.strip()
            if line.startswith('Name'):
                self.deck_name = line.split(' ', 1)[1].strip()
            elif line.startswith('Deck'):
                deck_list_started = True
            elif deck_list_started and line:
                # Adicionar as cartas ao deck
                quantity, card_name = line.split(' ', 1)
                quantity = int(quantity)
                
                # Buscar carta pelo nome usando a API da mtgsdk
                cards = Card.where(name=card_name.strip()).all()
                if not cards:
                    raise ValueError(f"Card '{card_name.strip()}' not found in the database.")
                
                # Assumindo que o primeiro resultado é o correto
                card = cards[0]
                for _ in range(quantity):
                    self.add_card(card)

    def determine_land_color(self, card):
        """
        Determines the color associated with a land card based on its name.
        """
        land_colors = {
            'Forest': {'G'},  # Green
            'Island': {'U'},  # Blue
            'Mountain': {'R'},  # Red
            'Plains': {'W'},  # White
            'Swamp': {'B'}   # Black
        }
        for land_name, colors in land_colors.items():
            if land_name in card.name:
                return colors
        return set()

    def add_card(self, card):
        """
        Adds a card to the deck if it meets the deck's requirements.
        """
        if len(self.cards) >= self.max_cards:
            raise ValueError("Deck already has the maximum number of cards.")
        
        if self.allowed_sets and card.set not in [set_.code for set_ in self.allowed_sets]:
            raise ValueError(f"Card from set {card.set} is not allowed in this deck.")
        
        if self.allowed_colors and card.colors is not None:
            if not set(card.colors).issubset(self.allowed_colors):
                raise ValueError(f"Card color(s) {card.colors} are not allowed in this deck.")

        if 'Land' in card.type or card.name in self.exception_cards:
            max_allowed = float('inf')
        else:
            max_allowed = self.max_cards_per_deck
        
        card_count = sum(1 for c in self.cards if c.name == card.name)
        if card_count >= max_allowed:
            raise ValueError(f"Cannot have more than {max_allowed} copies of {card.name} in the deck.")
        
        self.cards.append(card)

    def count_lands(self):
        """
        Counts the number of land cards in the deck.
        """
        return sum(1 for card in self.cards if 'Land' in card.type)

    def colors_in_deck(self):
        """
        Returns a set of all colors present in the non-land cards in the deck.
        """
        colors = set()
        for card in self.cards:
            if 'Land' not in card.type and card.colors:
                colors.update(card.colors)
        return colors

    def lands_matching_colors(self):
        """
        Returns a set of all land colors present in the deck.
        """
        land_colors = set()
        for card in self.cards:
            if 'Land' in card.type:
                land_colors.update(self.determine_land_color(card))
        return land_colors

    def remove_card(self, card):
        """
        Removes a card from the deck.
        """
        if card in self.cards:
            self.cards.remove(card)
        else:
            raise ValueError("Card is not in the deck.")

    def add_decklist(self, decklist):
        """
        Adds a list of cards to the deck based on a dictionary input.
        """
        for card_name, quantity in decklist.items():
            cards = Card.where(name=card_name).all()
            if not cards:
                raise ValueError(f"Card '{card_name}' not found in the database.")
            
            card = cards[0]
            for _ in range(quantity):
                self.add_card(card)

    def is_valid(self):
        """
        Checks if the deck meets the minimum and maximum card requirements, has the correct number of lands,
        and ensures every color in the deck has a corresponding land.

        Returns:
        --------
        bool
            True if the deck is valid according to the defined rules, False otherwise.
        """
        num_lands = self.count_lands()
        colors_in_deck = self.colors_in_deck()
        land_colors = self.lands_matching_colors()
        
        if not (self.min_cards <= len(self.cards) <= self.max_cards):
            return False
        
        if not (self.min_lands <= num_lands <= self.max_lands):
            return False
        
        if not colors_in_deck.issubset(land_colors):
            return False

        return True

    def determine_deck_colors_from_name(self, deck_name: str, df_colors: pd.DataFrame) -> Union[Dict[str, int], str]:
        """
        Determines the colors of the deck based on its name.

        Args:
            deck_name (str): The name of the deck, which can include color abbreviations or full color names.
            df_colors (pd.DataFrame): DataFrame containing color combinations and their binary values.

        Returns:
            Union[Dict[str, int], str]: A dictionary with the colors and their binary values (1 for present, 0 for absent) 
                                        or an error message if the color combination is not found.
        """
        deck_letters = ''.join([char for char in deck_name if char.isupper()])
        deck_letters_sorted = ''.join(sorted(deck_letters))

        if deck_letters_sorted in df_colors.index:
            return df_colors.loc[deck_letters_sorted].to_dict()

        for full_name in df_colors.index:
            if full_name.lower() in deck_name.lower():
                return df_colors.loc[full_name].to_dict()

        return "Combinação de cores não encontrada para o deck"

    def __len__(self):
        """
        Returns the number of cards currently in the deck.
        """
        return len(self.cards)

    def __repr__(self):
        """
        Returns a string representation of the deck.
        """
        allowed_sets = [set_.name for set_ in self.allowed_sets] if self.allowed_sets else "All sets allowed"
        allowed_colors = ', '.join(self.allowed_colors) if self.allowed_colors else "All colors allowed"
        num_lands = self.count_lands()
        return f"Deck({len(self.cards)} cards, {num_lands} lands, Language: {self.language}, Sets: {allowed_sets}, Colors: {allowed_colors})"
