from typing import List, Tuple
import tkinter as tk
from Board import Board
from MapDataClass import WallData
from Robot import Robot
from Wall import Direction
from copy import deepcopy


class RicochetRobotsUI:
    def __init__(
        self,
        master: tk.Tk,
        map_data: List[WallData],
        board_size: Tuple[int, int] = (16, 16),
    ):
        # Initialize board and UI elements
        self.board_size = board_size
        self.master = master
        self.board = Board(board_size)
        self.cell_size = 30  # size of every cell on the board
        self.steps = 0

        # Define robots, their station position, color and number.
        self.robots_original_positions = [
            Robot((2, 3), "red", 0),
            Robot((3, 3), "blue", 1),
            Robot((4, 3), "green", 2),
            # Robot((5, 3), "yellow", 3),
        ]
        self.current_robot = 0
        self.robots: List[Robot] = None

        # Canvas setup
        canvas_width = (self.board_size[0] + 1) * self.cell_size
        canvas_height = (self.board_size[1] + 1) * self.cell_size
        self.canvas = tk.Canvas(master, width=canvas_width, height=canvas_height)
        self.canvas.pack()
        self.init_ui()
        self.init_game(map_data)
        self.draw_robots()
        self.draw_walls()
        self.draw_goals()
        self.bind_keys()

    def init_ui(self):  # Draw grid lines
        for x in range(self.board_size[0] + 1):
            # Write indices at the bottom
            self.canvas.create_text(
                x * self.cell_size + self.cell_size / 2,
                self.board_size[1] * self.cell_size + self.cell_size / 2,
                text=str(x),
                font=("Arial", 12),
            )
            self.canvas.create_line(
                x * self.cell_size,
                0,
                x * self.cell_size,
                self.board_size[1] * self.cell_size,
            )

        for y in range(self.board_size[1] + 1):
            self.canvas.create_text(
                self.board_size[0] * self.cell_size + self.cell_size / 2,
                y * self.cell_size + self.cell_size / 2,
                text=str(y),
                font=("Arial", 12),
            )
            self.canvas.create_line(
                0,
                y * self.cell_size,
                self.board_size[0] * self.cell_size,
                y * self.cell_size,
            )

    def init_game(self, map_data: List[WallData]):  # Load map and robot position
        # Load map data
        for data in map_data:
            self.board.add_wall(
                data.x_pos, data.y_pos, Direction.from_int(data.direction)
            )

        self.robots = deepcopy(self.robots_original_positions)
        self.current_robot = 0

    def reset_game(self):
        self.steps = 0
        self.robots = deepcopy(self.robots_original_positions)
        self.current_robot = 0
        self.update_board()

    def draw_robots(self):
        # self.canvas.delete("robot")  # Clear existing robots
        for robot in self.robots:
            x1, y1 = (
                robot.position[0] * self.cell_size,
                robot.position[1] * self.cell_size,
            )
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=robot.color, tags="robot")

    def draw_walls(self):
        self.canvas.delete("wall")  # Clear existing walls
        for wall in self.board.walls:
            wall.draw(self.canvas, self.cell_size)

    def draw_goals(self):
        for goal in self.board.goals:
            goal.draw(self.canvas, self.cell_size)

    def update_board(self):  # Updates the board visually
        self.canvas.delete("wall")
        self.canvas.delete("robot")
        self.canvas.delete("goal")
        self.draw_walls()
        self.draw_goals()
        self.draw_robots()

    def move(self, direction: Direction):
        other_positions = [
            p.position for i, p in enumerate(self.robots) if i != self.current_robot
        ]
        robot = self.robots[self.current_robot]
        robot.move(direction, other_positions, self.board)
        self.steps = self.steps + 1
        print("steps: ", self.steps)
        self.update_board()

    def switch_robot(self, event):
        if event.char in "1234":
            self.current_robot = int(event.char) - 1

    def bind_keys(self):
        self.master.bind("<Up>", lambda e: self.move(Direction.NORTH))
        self.master.bind("<Down>", lambda e: self.move(Direction.SOUTH))
        self.master.bind("<Left>", lambda e: self.move(Direction.WEST))
        self.master.bind("<Right>", lambda e: self.move(Direction.EAST))
        self.master.bind("<Key>", self.switch_robot)
