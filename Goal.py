
class Goal:
    def __init__(self, x, y, robot_number, color):
        self.x = x
        self.y = y
        self.robot_number = robot_number
        self.color = color

    def draw(self, canvas, cell_size):
        # Define coordinates for drawing the goal
        x1 = self.x * cell_size
        y1 = self.y * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size
        # Draw a rectangle representing the goal
        canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline="black", tags="goal")






