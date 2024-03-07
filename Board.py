from typing import List, Tuple
from Goal import Goal
from Wall import Wall, Direction


class Board:
    def __init__(self, board_size: Tuple[int, int]):
        # Initialize the board with given size and an empty list of walls
        self.board_size: Tuple[int, int] = board_size
        self.walls: List[Wall] = []
        self.goals: List[Goal] = []

        # Add the goals and walls to the canvas
        self.create_goals()
        self.create_walls()

    def create_goals(self):
        self.add_goal(0, 7, 0, "red")
        self.add_goal(15, 0, 1, "blue")

    def add_goal(self, x: int, y: int, robot_number: int, color: str):
        goal = Goal(x, y, robot_number, color)
        self.goals.append(goal)

    def create_walls(self):
        return None

    def add_wall(
        self, x: int, y: int, direction: Direction
    ):  # Adds the wall to the canvas
        wall = Wall(x, y, direction)
        self.walls.append(wall)

    def is_wall(
        self, from_position: Tuple[int, int], to_position: Tuple[int, int]
    ):  # Check if there's a wall between two positions
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
            "NORTH": "SOUTH",
        }

        for wall in self.walls:  # Loops through all walls
            # print("Wall position:", (wall.x, wall.y), wall.direction.name,
            #      "\nPlayer position:", (x_from, y_from), move_direction, "\n \n")

            # Checks for walls that's facing the intended direction
            if (
                wall.x == x_from
                and wall.y == y_from
                and wall.direction.name == move_direction
            ):
                return True
            # Checks for walls that's facing the opposite direction
            elif (
                wall.x == x_to
                and wall.y == y_to
                and opposite_direction[wall.direction.name] == move_direction
            ):
                return True
        return False

    def is_on_goal(self, position: Tuple[int, int], robot_number: int):
        for goal in self.goals:
            if position == (goal.x, goal.y) and robot_number == goal.robot_number:
                #print(f"Robot {robot_number} reached its goal at {position}!")
                return True
        return False
