from Board import Board
from Robot import Robot
import tkinter as tk

from Wall import Wall


class RicochetRobotsUI:
    def __init__(self, master, board_size=(16, 16)):
        # Initialize board and UI elements
        self.board_size = board_size
        self.master = master
        self.board = Board(board_size)
        self.cell_size = 30  # size of every cell on the board

        # Canvas setup
        canvas_width = self.board_size[0] * self.cell_size
        canvas_height = self.board_size[1] * self.cell_size
        self.canvas = tk.Canvas(master, width=canvas_width, height=canvas_height)
        self.canvas.pack()

        # Define robots and current selected robot
        self.robots = [
            Robot((2, 3), "red"),
            Robot((3, 3), "blue"),
            Robot((4, 3), "green"),
            Robot((5, 3), "yellow")
        ]
        self.current_robot = 0

        self.init_ui()
        self.draw_robots()
        self.draw_walls()
        self.bind_keys()

    def init_ui(self):  # Draw grid lines

        for x in range(self.board_size[0] + 1):
            self.canvas.create_line(x * self.cell_size, 0, x * self.cell_size, self.board_size[1] * self.cell_size)
        for y in range(self.board_size[1] + 1):
            self.canvas.create_line(0, y * self.cell_size, self.board_size[0] * self.cell_size, y * self.cell_size)

    def draw_robots(self):
        self.canvas.delete("robot")  # Clear existing robots
        for robot in self.robots:
            x1, y1 = robot.position[0] * self.cell_size, robot.position[1] * self.cell_size
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=robot.color, tags="robot")

    def clear_board(self):
        self.canvas.delete("robot")
        self.draw_walls()  # Redraw walls

    def move(self, dx, dy):
        self.draw_walls()
        other_positions = [p.position for i, p in enumerate(self.robots) if i != self.current_robot]
        walls = {(wall.x, wall.y): wall.direction for wall in self.board.walls}
        robot = self.robots[self.current_robot]
        robot.move(dx, dy, self.board_size, other_positions, self.board)
        self.draw_robots()

    def switch_robot(self, event):
        if event.char in "1234":
            self.current_robot = int(event.char) - 1

    def bind_keys(self):
        self.master.bind("<Up>", lambda e: self.move(0, -1))
        self.master.bind("<Down>", lambda e: self.move(0, 1))
        self.master.bind("<Left>", lambda e: self.move(-1, 0))
        self.master.bind("<Right>", lambda e: self.move(1, 0))
        self.master.bind("<Key>", self.switch_robot)

    def draw_walls(self):
        self.canvas.delete("wall")  # Clear existing walls
        for wall in self.board.walls:
            wall.draw(self.canvas, self.cell_size)


def run_ricochet_robots_ui():
    root = tk.Tk()
    root.title("Ricochet Robots")
    game_ui = RicochetRobotsUI(root)
    root.mainloop()


if __name__ == '__main__':
    run_ricochet_robots_ui()