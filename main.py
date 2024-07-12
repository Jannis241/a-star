import math
import os
import random

leer_symbol = " "
block_symbol = "#"
start_symbol = "A"
target_symbol = "E"
path_symbol = "x"


class Node:
    def __init__(self, symbol) -> None:
        self.pos = None

        self.gCost = 1e9
        self.hCost = 1e9
        self.fCost = 1e9

        self.symbol = symbol
        self.parent = None


class Colors:
    RESET = "\033[0m"
    DARKGRAY = "\033[90m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    BLUE = "\033[94m"


class PathFinder:
    def __init__(self, width, height, minBlocks, maxBlocks, startEndMinAbstand) -> None:
        self.width = width  # int
        self.height = height  # int
        self.board = {}  # (x,y): node instance ---> zb leer, block, target, start, path (wenn er ihn gefunden hat)

        self.generateValidBoard(minBlocks, maxBlocks, startEndMinAbstand)

    def initBoard(self):
        # init all cells to be empty
        for x in range(self.width):
            for y in range(self.height):
                node = Node(leer_symbol)
                node.pos = (x, y)
                self.board[(x, y)] = node

        # setting the start, target and block symbols
        self.startNode = Node(start_symbol)
        self.startNode.pos = self.startPos

        self.targetNode = Node(target_symbol)
        self.targetNode.pos = self.targetPos

        self.board[self.startPos] = self.startNode
        self.board[self.targetPos] = self.targetNode

        for blockPos in self.blocks:
            blockNode = Node(block_symbol)
            blockNode.pos = blockPos
            self.board[blockPos] = blockNode

    def getNeighbors(self, node):
        nodes = []

        for x in range(-1, 2):  # -1 bis 1
            for y in range(-1, 2):
                if x != 0 and y != 0:  # (0,0) is just the current node

                    checkX = node.pos[0] + x
                    checkY = node.pos[1] + y

                    # check if the neigbor is in bounds
                    if checkX >= 0 and checkX < self.width and checkY >= 0 and checkY < self.height:
                        nodes.append(self.board[checkX, checkY])

        return nodes

    def retracePath(self, startNode, endNode):
        currentNode = endNode  # start at the end
        path = []
        while currentNode != startNode:
            path.append(currentNode)
            currentNode = currentNode.parent  # parent ist der node woher der current node kommt

        path.reverse()  # so we start at the beginning

        return path

    # vielleicht kann es hier ein error geben wenn der die surrounding nodes von einem an der ecke holen will
    def calculate(self):
        found = False
        alreadyEvaluated = set()
        stillAvailable = []

        stillAvailable.append(self.startNode)
        while len(stillAvailable) > 0:
            currentNode = stillAvailable[0]

            for node in stillAvailable:
                if node.fCost <= currentNode.fCost:
                    currentNode = node
            stillAvailable.remove(currentNode)
            alreadyEvaluated.add(currentNode)

            if currentNode.pos == self.targetPos:
                path = self.retracePath(self.startNode, self.targetNode)
                for node in path:
                    if node.symbol != target_symbol and node.symbol != start_symbol:
                        self.board[node.pos] = Node(path_symbol)
                return True

            for neighbor in self.getNeighbors(currentNode):
                if neighbor.symbol != block_symbol and not neighbor in alreadyEvaluated:
                    newCostToNeighbor = currentNode.gCost + self.calcDistanceOfTwoPositions(currentNode.pos, neighbor.pos)

                    if newCostToNeighbor < neighbor.gCost or not neighbor in stillAvailable:
                        neighbor.gCost = newCostToNeighbor
                        neighbor.hCost = self.calcDistanceOfTwoPositions(neighbor.pos, self.targetNode.pos)
                        neighbor.fCost = neighbor.gCost + neighbor.hCost
                        neighbor.parent = currentNode

                        if not neighbor in stillAvailable:
                            stillAvailable.append(neighbor)

    def draw(self):
        # os.system("cls" if os.name == "nt" else "clear")

        # Oberer Rand
        print("_" * (self.width + 2))

        for y in range(self.height):
            row = "|"
            for x in range(self.width):
                node = self.board[(x, y)]
                symbol = node.symbol
                if symbol == block_symbol:
                    row += Colors.DARKGRAY + symbol + Colors.RESET
                elif symbol == start_symbol:
                    row += Colors.GREEN + symbol + Colors.RESET
                elif symbol == target_symbol:
                    row += Colors.RED + symbol + Colors.RESET
                elif symbol == path_symbol:
                    row += Colors.BLUE + symbol + Colors.RESET
                else:
                    row += symbol
            row += "|"
            print(row)

        # Unterer Rand
        print("_" * (self.width + 2))
        print(f"StartPos: {self.startPos}, TargetPos: {self.targetPos}")

    def start(self):
        # loop
        self.initBoard()
        found = False
        self.draw()
        while not found:
            found = self.calculate()
        self.draw()

    def calcDistanceOfTwoPositions(self, pos1, pos2):
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]

        distance = math.sqrt(dx**2 + dy**2)

        return distance

    def generateValidBoard(self, minBlocks, maxBlocks, startEndMinAbstand):
        anzahlBlocks = random.randint(minBlocks, maxBlocks)

        # generate start and target position while having the having the min abstand
        while True:
            self.startPos = (random.randint(1, self.width - 1), random.randint(1, self.height - 1))
            self.targetPos = (random.randint(1, self.width - 1), random.randint(1, self.height - 1))
            distance = self.calcDistanceOfTwoPositions(self.startPos, self.targetPos)
            if distance >= startEndMinAbstand:
                break

        self.blocks = []
        # generate blocks
        for i in range(anzahlBlocks):
            while True:
                randomPos = (random.randint(0, self.width), random.randint(0, self.height))
                if randomPos != self.startPos and randomPos != self.targetPos and not randomPos in self.blocks:
                    self.blocks.append(randomPos)
                    break


astar = PathFinder(10, 5, 2, 10, 3)
astar.start()


def func(x):
    return x + 1


items = [1, 5, 8]

items = list(map(func, items))
print(items)
