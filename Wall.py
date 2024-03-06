from enum import Enum


class Direction(Enum):  # The side of the field the wall is located at
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4

    # overloading '~' operator
    def __invert__(self):
        if self == Direction.NORTH:
            return Direction.SOUTH
        if self == Direction.SOUTH:
            return Direction.NORTH
        if self == Direction.EAST:
            return Direction.WEST
        if self == Direction.WEST:
            return Direction.EAST

class Wall:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def draw(self, canvas, cell_size):  # Draw the wall on the canvas based on position and direction
        if self.direction == Direction.NORTH:
            canvas.create_line(self.x * cell_size, self.y * cell_size,
                               (self.x + 1) * cell_size, self.y * cell_size,
                               width=4, fill="black")
        elif self.direction == Direction.SOUTH:
            canvas.create_line(self.x * cell_size, (self.y + 1) * cell_size,
                               (self.x + 1) * cell_size, (self.y + 1) * cell_size,
                               width=4, fill="black")
        elif self.direction == Direction.EAST:
            canvas.create_line((self.x + 1) * cell_size, self.y * cell_size,
                               (self.x + 1) * cell_size, (self.y + 1) * cell_size,
                               width=4, fill="black")
        elif self.direction == Direction.WEST:
            canvas.create_line(self.x * cell_size, self.y * cell_size,
                               self.x * cell_size, (self.y + 1) * cell_size,
                               width=4, fill="black")
