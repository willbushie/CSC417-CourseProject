class card:
    """
    Creates a single card object.
    """
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def getInfo(self):
        """
        This method returns a string of format `rank of suit`.
        """
        return f"{self.rank} of {self.suit}"