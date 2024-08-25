class Plays:
    """
    A class to track the plays made by a player.
    
    Attributes:
    -----------
    played : int
        The number of cards successfully played (put on the battlefield).
    not_played : int
        The number of cards that could not be played (remained in hand or discarded).
    """
    
    def __init__(self):
        self.played = 0
        self.not_played = 0

    def add_played(self):
        """Incrementa o número de cartas jogadas."""
        self.played += 1

    def add_not_played(self):
        """Incrementa o número de cartas não jogadas."""
        self.not_played += 1

    def count_played(self):
        """Retorna o número de cartas jogadas."""
        return self.played

    def count_not_played(self):
        """Retorna o número de cartas não jogadas."""
        return self.not_played
