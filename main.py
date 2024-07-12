import os
import random

leer_symbol = " "
block_symbol = "#"
start_symbol = "S"
target_symbol = "E"
path_symbol = "x"


class PathFinder:
    def __init__(self, width, height, minBlocks, maxBlocks) -> None:
        self.width = width  # int
        self.height = height  # int
        self.board = {}  # (x,y): state ---> zb leer, block, target, start, path (wenn er ihn gefunden hat)

        self.generateValidBoard(minBlocks, maxBlocks)

    def initBoard(self):

        # init all cells to be empty
        for x in range(self.width):
            for y in range(self.height):
                self.board[(x, y)] = leer_symbol

        # setting the start, target and block symbols
        self.board[self.startPos] = start_symbol
        self.board[self.targetPos] = target_symbol

        for blockPos in self.blocks:
            self.board[blockPos] = block_symbol

    def calculate(self):
        return True

    def draw(self):
        os.system("cls")

        for y in range(self.height):
            row = ""
            for x in range(self.width):
                row += self.board[(x, y)]
            print(row)

    def start(self):
        # loop
        self.initBoard()
        found = False
        while not found:
            found = self.calculate()
            self.draw()

    def generateValidBoard(self, minBlocks, maxBlocks):
        anzahlBlocks = random.randint(minBlocks, maxBlocks, startEndMinAbstand)

        # generate start and target position while having the having the min abstand
        self.startPos = (1, 1)  # (x,y)
        self.targetPos = (50, 5)  # (x,y)

        self.blocks = []
        # generate blocks
        for i in range(anzahlBlocks):
            while True:
                randomPos = (random.randint(0, self.width), random.randint(0, self.height))
                if randomPos != self.startPos and randomPos != self.targetPos and not randomPos in self.blocks:
                    self.blocks.append(randomPos)
                    break


astar = PathFinder(110, 15, 60, 100)
astar.start()
