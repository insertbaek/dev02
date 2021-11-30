import random
import math
class Cell:
    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y

        self.walls = {
            'n' : True,
            'e' : True,
            's' : True,
            'w' : True
        }

        self.visited = False

class Maze:
    def __init__(self, width = 5, height = 5):
        self.cells = self.generateMaze(width, height)
        self.solution = []
        self.solution2 = []

    def generateMaze(self, width, height):
        generateCells = []
        for x in range(0, width, 1):
            generateCells.insert(x,[])
            for y in range(0, height, 1):
                generateCells[x].insert(y,Cell(x, y))

        startX = math.floor(random.randrange(width))
        startY =  math.floor(random.randrange(height))

        self.visit(generateCells[startX][startY])

        solution = solve(width - 1, height - 1, 0, 0)
        solution2 = solve(0, height - 1, width-1, 0)

        if solution.length == solution2.length:
            self.solution = solution
            self.solution2 = solution2
            return generateCells
        else:
            return generateMaze(width, height)

    def getOptions(self, cell, walls):
        options = []

        def checkOption(x, y):

            if (walls):
                if ((y < cell.y and cell.walls.n) or
                    (x > cell.x and cell.walls.e) or
                    (y > cell.y and cell.walls.s) or
                    (x < cell.x and cell.walls.w)):
                    return

            if (cells[x] and cells[x][y] and not cells[x][y].visited):
                options.push(cells[x][y])
        print(cell.x)
        checkOption(cell.x, cell.y - 1)
        checkOption(cell.x + 1, cell.y)
        checkOption(cell.x, cell.y + 1)
        checkOption(cell.x - 1, cell.y)

        return options

    def visit(self, cell):
        cell.visited = True

        options = self.getOptions(self,cell)

        while (options.length > 0):
            index =  math.floor(random.randrange(width)*options.length)
            nextCell = options[index]

            if cell.y > nextCell.y:
                cell.walls.n = false
                visit(nextCell, "s")
            elif cell.x < nextCell.x:
                cell.walls.e = false
                visit(nextCell, "w")
            elif cell.y < nextCell.y:
                cell.walls.s = false
                visit(nextCell, "n")
            elif cell. x > nextCell.x:
                cell.walls.w = false
                visit(nextCell, "e")

            options = getOptions(cell)

    def solve(startX, startY, endX, endY):
        startX = startX or 0
        startY = startY or 0
        endX = endX == null and width - 1 or endX
        endY = endY == null and height - 1 or endY

        for x in range(0, cells.length, 1):
            for y in range(0, cells[x].length, 1):
                cells[x][y].visited = false

        solution = []
        cell = cells[startX][startY]
        options = []

        while ((cell.x != endX) or (cell.y != endY)):
            cell.visited = true
            options = getOptions(cell, true)

            if (options.length == 0):
                cell = solution.pop()
            else:
                solution.push(cell)
                cell = options[0]

        solution.push(cell)

        return solution

    def getData():
        print(self.cells)

if __name__ == '__main__':
    instance = Maze()
    instance.getData()