from enum import Enum
from AIInterface import AIInterface
from BFSai import BFSai
from typing import List, Tuple
from MapDataClass import WallData
from ui import RicochetRobotsUI
import json
import tkinter as tk


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


def run_ricochet_robots_ui(map_data):
    root = tk.Tk()
    root.title("Ricochet Robots")
    game_ui = RicochetRobotsUI(root, map_data)
    ai_interface = AIInterface(game_ui)

    root.after(500, BFSai.build_solution_and_play, ai_interface)
    root.mainloop()


def show_game_ui():
    root = tk.Tk()
    root.title("Ricochet Robots Menu")
    _ = RicochetRobotMenu(root)
    root.mainloop()


if __name__ == "__main__":
    show_game_ui()
