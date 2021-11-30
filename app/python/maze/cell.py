class Cell:
    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y

        self.walls = {
            n : true,
            e : true,
            s : true,
            w : true
        }

        self.visited = false
