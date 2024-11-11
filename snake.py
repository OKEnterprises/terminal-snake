import time
import random
from typing import Literal

type Coord = tuple[int, int]
type Direction = Literal["N", "S", "E", "W"]

class Snake:
    def __init__(self, length=1):
        self.length = 1
        self.char = "🐍"
        self.head = (0, 0)
        self.body = []
        self.dir = "E"

    def set_dir(self, direction: Direction):
        self.dir = direction

    def get_next_coord(self) -> Coord:
        row, col = self.head
        if self.dir == "N":
            row -= 1
        elif self.dir == "S":
            row += 1
        elif self.dir == "E":
            col += 1
        elif self.dir == "W":
            col -= 1
        return row, col

    def move(self, coord: Coord, grow=False):
        if not grow and self.length < 1:
            self.body.pop()
        else:
            self.length += 1
        self.body.append(self.head)
        self.head = coord

class Gameboard:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.board = [
            [" " for i in range(self.width)]
                for i in range(self.height)
        ]

    def __str__(self) -> str:
        return "\n".join(["".join(row) for row in self.board])

    def place_apple(self):
        row, col = 0, 0
        while self.board[row][col] == "🐍":
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
        self.board[row][col] = "🍎"

    def place_snake(self, s: Snake):
        row_0, col_0 = s.head
        self.board[row_0][col_0] = s.char
        for segment in s.body:
            row, col = segment
            self.board[row][col] = s.char

    def get(self, row: int, col: int) -> str:
        return self.board[row][col]


class Game:
    def __init__(self, width=10, height=10):
        self.over = False
        self.board = Gameboard(width, height)
        self.s = Snake()
        self.board.place_apple()

    def mainloop(self):
        while self.over == False:
            self.tick()
            time.sleep(0.2)
        print(f"Game over! Score: {self.s.length}")

    def tick(self):
        row, col = self.s.get_next_coord()
        if any([row < 0, row >= self.board.height, col < 0, col >= self.board.width]) or self.board.get(row, col) == "🐍":
            self.over = True
            return
        grow = self.board.board[row][col] == "🍎"
        self.s.move((row, col), grow=grow)
        self.board.place_snake(self.s)
        if grow: self.board.place_apple()
        print(self.board)

if __name__ == "__main__":
    import sys
    g = Game(int(sys.argv[1]), int(sys.argv[2]))
    g.mainloop()
