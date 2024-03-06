from typing import Tuple, List

from Board import Board
from Wall import Direction
from typing import NamedTuple


class AvailableMove(NamedTuple):
    final_position: Tuple[int, int]
    direction: Direction


class Robot:
    def __init__(self, position: Tuple[int, int], color: str, robot_id: int):
        self.position = position
        self.color = color
        self.robot_id = robot_id

    @staticmethod
    def available_moves(
        current_position: Tuple[int, int],
        board: Board,
        other_robots_positions: List[Tuple[int, int]],
    ) -> List[AvailableMove]:
        """Return a list of available moves for the robot.

        Parameters:
        current_position (Tuple[int, int]): The current position of the robot.
        board (Board): The board object containing the walls and goals.
        other_robots_positions (List[Tuple[int, int]]): The positions of the other robots.

        Returns:
        List[AvailableMove]: A list of available moves for the robot.
        """
        available_moves = []
        for direction in Direction:
            final_position = Robot.find_final_position(
                current_position, direction, board, other_robots_positions
            )

            # If the final position is different from the current position, add the move to the list
            if final_position != current_position:
                available_moves.append(AvailableMove(final_position, direction))

        return available_moves

    @staticmethod
    def find_final_position(
        current_position: Tuple[int, int],
        direction: Direction,
        board: Board,
        other_robots_positions: List[Tuple[int, int]],
    ) -> Tuple[int, int]:
        """Given a direction for a robot to move, return the final position after moving.

        Parameters:
        current_position (Tuple[int, int]): The current position of the robot.
        direction (Direction): The direction to move the robot.
        board (Board): The board object containing the walls and goals.
        other_robots_positions (List[Tuple[int, int]]): The positions of the other robots.

        Returns:
        Tuple[int, int]: The final position of the robot after moving.
        """
        final_position = current_position
        moving = True
        while moving:
            x, y = final_position
            dx, dy = direction.value
            new_x, new_y = x + dx, y + dy

            # Check if the new position is within the board boundaries
            if 0 <= new_x < board.board_size[0] and 0 <= new_y < board.board_size[1]:

                # Check if new position is not another robot and not blocked by a wall
                if (new_x, new_y) not in other_robots_positions and not board.is_wall(
                    final_position, (new_x, new_y)
                ):
                    final_position = (new_x, new_y)  # move the robot
                else:
                    moving = (
                        False  # Stop moving if another robot or a wall blocks the path
                    )
            else:
                moving = False  # Stop moving if the edge of the board is reached

        return final_position

    def move(
        self,
        direction: Direction,
        other_robots_positions: List[Tuple[int, int]],
        board: Board,
    ) -> bool:
        """Move the robot in a given direction.

        Parameters:
        direction (Direction): The direction to move the robot.
        other_robots_positions (List[Tuple[int, int]]): The positions of the other robots.
        board (Board): The board object containing the walls and goals.

        Returns:
        bool: True if the robot is on its goal after moving, False otherwise.
        """

        final_position = Robot.find_final_position(
            self.position, direction, board, other_robots_positions
        )
        self.position = final_position
        return board.is_on_goal(self.position, self.robot_id)
