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
        self.gCost = None
        self.hCost = None
        self.fCost = None
        self.surroundingNodes = []
        self.explored = False
        self.symbol = symbol


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
        startNode = Node(start_symbol)
        startNode.pos = self.startPos

        targetNode = Node(target_symbol)
        targetNode.pos = self.targetPos

        self.board[self.startPos] = startNode
        self.board[self.targetPos] = targetNode

        for blockPos in self.blocks:
            blockNode = Node(block_symbol)
            blockNode.pos = blockPos
            self.board[blockPos] = blockNode

    def getSurroundingNodes(self, pos):
        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        nodes = []

        for offset in offsets:
            try:
                newPos = (pos[0] + offset[0], pos[1] + offset[1])
                node = self.board[newPos]
                nodes.append(node)
            except:
                pass

        return nodes

    # vielleicht kann es hier ein error geben wenn der die surrounding nodes von einem an der ecke holen will
    def calculate(self):
        found = False
        currentNodePos = self.startPos
        while not found:
            surroundingNodes = self.getSurroundingNodes(currentNodePos)  # returns node instance
            validNeighborNodes = []
            print()
            print()
            print()
            print()
            print()
            print()
            print()
            print()
            print()
            print()
            print()
            print()
            self.draw()
            print("Current node: ", currentNodePos)
            print("Surrounding Nodes found: ", len(surroundingNodes))

            print("All surrounding neighbor positions: ")
            for n in surroundingNodes:
                print(f"neighbor at: {n.pos}, Symbol: {n.symbol}, Explored: {n.explored}")
            if len(surroundingNodes) == 0:
                exit()
            if len(surroundingNodes) > 0:
                for neighbor in surroundingNodes:

                    print("")
                    # calc g cost -> dst to the starting node
                    # calc h cost -> dst to the target node
                    # clac f cost -> h cost * g cost
                    # the smallest f cost node is choosen -> marked as closed (set it as currentNode)
                    # if 2 or more nodes have the same f cost --> look at the h cost (dst to target) and pick the one with the lowest

                    # sobald eine node explored wurde wird sie als "closed" makiert (rot im video) -> das heißt die muss man nicht mehr exploren
                    # es wird immer das node mit der niedrigsten f cost "explored", das node muss nicht umbedingt neighbor vom currentNode sein,
                    # sondern kann überall sein -> das heißt man kann ganz links sein, merkt aber die f-cost wird immer höher, und plötzlich ist die
                    # f-cost ganz rechts niedriger als alle ganz links, dann "explored" man natürlich das node ganz rechts
                    # !! nodes die schon explored wurden werden natürlich nicht nochmal explored
                    if neighbor.pos != None:  # out of board
                        if neighbor.symbol != block_symbol:
                            neighbor.gCost = self.calcDistanceOfTwoPositions(neighbor.pos, self.startPos)
                            neighbor.hCost = self.calcDistanceOfTwoPositions(neighbor.pos, self.targetPos)
                            neighbor.fCost = neighbor.gCost * neighbor.hCost
                            validNeighborNodes.append(neighbor)
                            print(f"currently checking node at: {neighbor.pos}, symbol: {neighbor.symbol}, already explored: {neighbor.explored}, f-cost: {neighbor.fCost}")
                print(f"found: {len(validNeighborNodes)} valid neighbor nodes that could be explored!")

                lowestFCost = 10e10
                lowestFCostNode = None
                for neighbor in validNeighborNodes:
                    if neighbor.fCost != None:
                        if neighbor.fCost < lowestFCost:
                            if not neighbor.explored:
                                lowestFCostNode = neighbor
                print(f"Node with the lowest f-cost is at: {lowestFCostNode.pos}, symbol: {lowestFCostNode.symbol}, f-cost: {lowestFCostNode.fCost}")

                if lowestFCostNode != None:
                    lowestFCostNode.explored = True
                    currentNodePos = lowestFCostNode.pos
                    print("setting the current node to: ", currentNodePos)
                    if currentNodePos == self.targetPos:
                        print("found the target pos!")
                        return True
                    self.board[currentNodePos] = Node(path_symbol)
                
                print("------------- end of iteration ---------------------")

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
        while not found:
            self.draw()
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


astar = PathFinder(110, 15, 100, 130, 90)
astar.start()
