from mtgsdk import Card

class Battlefield:
    """
    A class to represent the battlefield, where lands are played and produce mana.

    Attributes:
    -----------
    lands : list of Card
        The lands currently on the battlefield.
    """

    def __init__(self):
        self.lands = []

    def add_land(self, card: Card):
        """
        Adds a land to the battlefield.

        Parameters:
        -----------
        card : Card
            The land card to be added to the battlefield.
        """
        self.lands.append(card)

    def calculate_mana_pool(self) -> int:
        """
        Calculates the total mana pool based on the lands on the battlefield.
        
        Returns:
        --------
        int
            The total available mana from all lands on the battlefield.
        """
        return len(self.lands) 