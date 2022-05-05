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

    def getSuit(self):
        """
        Return a string of the card suit.
        """
        return self.suit

    def getRank(self):
        """
        Return a string of the card rank.
        """
        return self.rank

    def getInfoSimple(self):
        """
        This method returns a simple form of the cards rank and suit. `1c` is the One of Clubs. `Ad` is the Ace of Diamonds.
        """
        letter = ["One","Two","Three","Four","Five","Six","Seven","Eight","Nine"]
        number = ["1","2","3","4","5","6","7","8","9"]
        simple = ""
        if (self.getRank() in letter):
            simple = simple + number[(letter.index(self.getRank()))]
        elif (self.getRank() not in letter):
            simple = simple + (self.getRank())[:1]
        simple = simple + ((self.getSuit())[:1]).lower()
        return simple
