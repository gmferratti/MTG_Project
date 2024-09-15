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
    
    def calculate_mana_pool_per_color(self) -> dict:
        """
        Calculates the mana pool per color based on the lands on the battlefield.

        Returns:
        --------
        dict
            A dictionary with the amount of mana available for each color.
        """
        mana_pool = {'C': 0, 'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0}
        
        for land in self.lands:
            if land.color_identity:
                for color in land.color_identity:
                    if color in mana_pool:
                        mana_pool[color] += 1
        return mana_pool