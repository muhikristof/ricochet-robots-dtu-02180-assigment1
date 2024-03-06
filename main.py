from enum import Enum
import json
from typing import List
from AIInterface import AIInterface, dumb_ai_test
from Board import Board
from MapDataClass import WallData
from Robot import Robot
import tkinter as tk

from Wall import Wall, Direction


class RicochetRobotMenu:
    class MapName(Enum):
        DEFAULT = "default"
        EASY = "easy"
        MEDIUM = "medium"
        HARD = "hard"

    def __init__(self, master):
        self.master = master
        self.master.geometry("300x300")
        self.init_ui()

    def init_ui(self):
        tk.Button(
            self.master,
            text="Default map",
            height="3",
            command=lambda: self.start_game(self.MapName.DEFAULT),
        ).pack(side="top", fill="x")
        tk.Button(
            self.master,
            text="Easy map",
            height="3",
            command=lambda: self.start_game(self.MapName.EASY),
        ).pack(side="top", fill="x")
        tk.Button(
            self.master,
            text="Medium map",
            height="3",
            command=lambda: self.start_game(self.MapName.MEDIUM),
        ).pack(side="top", fill="x")
        tk.Button(
            self.master,
            text="Hard map",
            height="3",
            command=lambda: self.start_game(self.MapName.HARD),
        ).pack(side="top", fill="x")

    def start_game(self, map_name: MapName):
        self.master.destroy()
        run_ricochet_robots_ui(self.load_map(map_name))

    def load_map(self, map_name: MapName) -> List[WallData]:
        with open(str.format("maps/{}.json", map_name.value), "r") as f:
            return json.loads(f.read(), object_hook=WallData.to_object)


class RicochetRobotsUI:
    def __init__(self, master, map_data: List[WallData], board_size=(16, 16)):
        # Initialize board and UI elements
        self.board_size = board_size
        self.master = master
        self.board = Board(board_size)
        self.cell_size = 30  # size of every cell on the board
        self.steps = 0

        # Canvas setup
        canvas_width = self.board_size[0] * self.cell_size
        canvas_height = self.board_size[1] * self.cell_size
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
            self.canvas.create_line(
                x * self.cell_size,
                0,
                x * self.cell_size,
                self.board_size[1] * self.cell_size,
            )
        for y in range(self.board_size[1] + 1):
            self.canvas.create_line(
                0,
                y * self.cell_size,
                self.board_size[0] * self.cell_size,
                y * self.cell_size,
            )

    def init_game(self, map_data: List[WallData]):  # Load map and robot position

        # Load map data
        for data in map_data:
            self.board.add_wall(data.x_pos, data.y_pos, Direction(data.direction))

        # Define robots, their station position, color and number.
        self.robots = [
            Robot((2, 3), "red", 0),
            Robot((3, 3), "blue", 1),
            Robot((4, 3), "green", 2),
            Robot((5, 3), "yellow", 3),
        ]
        self.current_robot = 0

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

    def move(self, dx, dy):
        other_positions = [
            p.position for i, p in enumerate(self.robots) if i != self.current_robot
        ]
        robot = self.robots[self.current_robot]
        robot.move(dx, dy, self.board_size, other_positions, self.board)
        self.steps = self.steps + 1
        print("steps: ", self.steps)
        self.update_board()

    def switch_robot(self, event):
        if event.char in "1234":
            self.current_robot = int(event.char) - 1

    def bind_keys(self):
        self.master.bind("<Up>", lambda e: self.move(0, -1))
        self.master.bind("<Down>", lambda e: self.move(0, 1))
        self.master.bind("<Left>", lambda e: self.move(-1, 0))
        self.master.bind("<Right>", lambda e: self.move(1, 0))
        self.master.bind("<Key>", self.switch_robot)


def show_game_ui():
    root = tk.Tk()
    root.title("Ricochet Robots Menu")
    menu_ui = RicochetRobotMenu(root)
    root.mainloop()


def run_ricochet_robots_ui(map_data):
    root = tk.Tk()
    root.title("Ricochet Robots")
    game_ui = RicochetRobotsUI(root, map_data)
    ai_interface = AIInterface(game_ui)

    # Initialize the AI. This is just a dummy test that moves a robot to goal. But the interaction should be similar.
    # When building the AI, replace with root.after(0, method to run AI, ai_interface)
    root.after(1000, dumb_ai_test, ai_interface)
    root.mainloop()


if __name__ == "__main__":
    show_game_ui()
