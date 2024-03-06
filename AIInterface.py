import time

from UI import RicochetRobotsUI
from Wall import Direction


class AIInterface:
    def __init__(self, game_instance: RicochetRobotsUI):
        self.game_instance = game_instance

    def move_robot(self, robot_id: int, direction: Direction):
        """
        Moves a specified robot in a given direction.

        :param robot_id: The ID of the robot to move.
        :param direction: The direction from the Direction enum.
        """

        # Map directions to their (dx, dy) changes
        direction_map = {
            Direction.NORTH: (0, -1),
            Direction.SOUTH: (0, 1),
            Direction.EAST: (1, 0),
            Direction.WEST: (-1, 0),
        }
        dx, dy = direction_map[direction]

        # Set the current robot and move it
        self.game_instance.current_robot = robot_id
        self.game_instance.move(dx, dy)
        self.game_instance.update_board()

        # Use Board's is_on_goal method to check if the robot is on its goal
        robot = self.game_instance.robots[robot_id]
        on_goal = self.game_instance.board.is_on_goal(robot.position, robot.robot_id)

        self.game_instance.master.update_idletasks()  # Update UI after move

        return robot.position, on_goal


def dumb_ai_test(game_interface: AIInterface):
    # Move robot 2 up and then right.

    # Move robot 2 up
    robot_id = 1
    new_position, on_goal = game_interface.move_robot(
        robot_id, Direction.NORTH
    )  # THis one line is what the AI would use
    print(
        f"Robot {robot_id} moved to {new_position}. On goal: {'Yes' if on_goal else 'No'}"
    )
    time.sleep(1)  # Just to see it move

    # Move robot 2 right
    new_position, on_goal = game_interface.move_robot(
        robot_id, Direction.EAST
    )  # Move right
    print(
        f"Robot {robot_id} moved to {new_position}. On goal: {'Yes' if on_goal else 'No'}"
    )
    time.sleep(1)  # Just to see it move
