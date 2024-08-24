from mtgsdk import Card, Set

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
        
        # Verificar cores apenas se card.colors não for None
        if self.allowed_colors and card.colors is not None:
            if not set(card.colors).issubset(self.allowed_colors):
                raise ValueError(f"Card color(s) {card.colors} are not allowed in this deck.")

        # Verificar exceções de quantidade de cópias
        if 'Land' in card.type or card.name in self.exception_cards:
            max_allowed = float('inf')  # Permite infinitas cópias para terrenos ou cartas de exceção
        else:
            max_allowed = self.max_cards_per_deck
        
        # Contagem baseada no nome do card (e não na instância do objeto)
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
            
            card = cards[0]  # Assume que o primeiro card encontrado é o correto
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
        
        # Verifica se o número de cartas está dentro dos limites
        if not (self.min_cards <= len(self.cards) <= self.max_cards):
            return False
        
        # Verifica se o número de terrenos está dentro dos limites
        if not (self.min_lands <= num_lands <= self.max_lands):
            return False
        
        # Verifica se todas as cores no deck têm um terreno correspondente
        if not colors_in_deck.issubset(land_colors):
            return False

        return True

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