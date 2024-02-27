from Wall import Wall, Direction


class Board:
    def __init__(self, board_size):
        # Initialize the board with given size and an empty list of walls
        self.board_size = board_size
        self.walls = []

        # Add the walls to the canvas
        self.create_walls()

    def create_walls(self):
        self.add_wall(2, 2, Direction.NORTH)
        self.add_wall(6, 7, Direction.EAST)
        self.add_wall(3, 5, Direction.WEST)
        self.add_wall(8, 3, Direction.SOUTH)
        self.add_wall(10, 10, Direction.NORTH)
        self.add_wall(12, 12, Direction.WEST)
        self.add_wall(8, 6, Direction.EAST)
        self.add_wall(4, 10, Direction.SOUTH)
        self.add_wall(5, 14, Direction.WEST)
        self.add_wall(11, 8, Direction.NORTH)
        self.add_wall(13, 5, Direction.EAST)
        self.add_wall(9, 12, Direction.WEST)
        self.add_wall(6, 3, Direction.SOUTH)
        self.add_wall(14, 14, Direction.NORTH)
        self.add_wall(2, 8, Direction.WEST)
        self.add_wall(4, 4, Direction.EAST)
        self.add_wall(12, 2, Direction.SOUTH)
        self.add_wall(7, 11, Direction.NORTH)
        self.add_wall(15, 7, Direction.WEST)
        self.add_wall(13, 9, Direction.EAST)
        self.add_wall(0, 5, Direction.SOUTH)
        self.add_wall(16, 10, Direction.WEST)
        self.add_wall(8, 0, Direction.SOUTH)
        self.add_wall(5, 15, Direction.NORTH)

    def add_wall(self, x, y, direction):  # Adds the wall to the canvas
        wall = Wall(x, y, direction)
        self.walls.append(wall)

    def is_wall(self, from_position, to_position):  # Check if there's a wall between two positions
        x_from, y_from = from_position
        x_to, y_to = to_position
        dx = x_to - x_from
        dy = y_to - y_from

        # Get the direction of the move
        if dx > 0:
            move_direction = "EAST"
        elif dx < 0:
            move_direction = "WEST"
        elif dy > 0:
            move_direction = "SOUTH"
        else:
            move_direction = "NORTH"

        # Get the opposite directions for wall comparison
        opposite_direction = {
            "EAST": "WEST",
            "WEST": "EAST",
            "SOUTH": "NORTH",
            "NORTH": "SOUTH"
        }

        for wall in self.walls:  # Loops through all walls
            # print("Wall position:", (wall.x, wall.y), wall.direction.name,
            #      "\nPlayer position:", (x_from, y_from), move_direction, "\n \n")

            # Checks for walls that's facing the intended direction
            if wall.x == x_from and wall.y == y_from and wall.direction.name == move_direction:
                return True
            # Checks for walls that's facing the opposite direction
            elif wall.x == x_to and wall.y == y_to and opposite_direction[wall.direction.name] == move_direction:
                return True
        return False
