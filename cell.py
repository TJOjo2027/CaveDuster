class Cell:
    # Constructor initializing the cell
    # defaults the status of if its a mine or not
    # defualts the weight of the cell
    # defaults the status of if its been clicked or not
    def __init__(self, isMine, weight, isCovered):
        self.isMine = isMine
        self.weight = weight
        self.isCovered = isCovered

    # Getter for the Cell Weight
    def getCellWeight(self):
        return self.weight