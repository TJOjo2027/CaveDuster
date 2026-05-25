from cell import Cell
import random

class MineGrid:
    # initializes a grid of cells that form the minesweeper board
    def __init__(self, numRows, numCols):
        self.mineGrid = []
        self.numRows = numRows
        self.numCols = numCols

        # populate mineGrid with default cells
        # mines placed on first click
        for i in range(numRows):
            row = []
            for j in range(numCols):
                row.append(Cell(False, 0, True))
            self.mineGrid.append(row)

    def initializeMines(self, safeRow, safeCol):
        self.placeMines(safeRow, safeCol)
        self.findCellWeight()

    def getCell(self, row, col):
        return self.mineGrid[row][col]

    def findCellWeight(self):
        for row in range(self.numRows):
            for col in range(self.numCols):
                cell = self.getCell(row, col)

                if cell.isMine:
                    continue

                cellParams = [[row - 1, col - 1], [row - 1, col], [row - 1, col + 1],
                              [row, col - 1],                         [row, col + 1],
                              [row + 1, col - 1], [row + 1, col], [row + 1, col + 1]]

                for neighborRow, neighborCol in cellParams:
                    if (neighborRow < 0 or
                        neighborRow >= self.numRows or
                        neighborCol < 0 or
                        neighborCol >= self.numCols):
                        continue

                    neighborCell = self.getCell(neighborRow, neighborCol)
                    if neighborCell.isMine:
                        cell.weight += 1

    def placeMines(self, safeRow, safeCol):
        for row in range(self.numRows):
            for col in range(self.numCols):
                if row == safeRow and col == safeCol:
                    continue # never mine the first click cell
                jackpot = random.randint(1, 10)
                if jackpot == 7:
                    self.mineGrid[row][col].isMine = True

    # function for pre-GUI debug
    def printMineGrid(self):
        for row in range(self.numRows):
            for col in range(self.numCols):
                cell = self.mineGrid[row][col]
                print(f"Coordinates of Grid -> [{row}, {col}]")
                if cell.isMine:
                    print("MINE HERE!\n")
                else:
                    print("no mine :)")
                    print(f"Cell Weight -> {cell.weight} mines are around you!\n")