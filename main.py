import tkinter as tk
from ui import RicochetRobotMenu


def show_game_ui():
    root = tk.Tk()
    root.title("Ricochet Robots Menu")
    _ = RicochetRobotMenu(root)
    root.mainloop()


if __name__ == "__main__":
    show_game_ui()
