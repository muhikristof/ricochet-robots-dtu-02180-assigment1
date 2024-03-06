from typing import Tuple, List

from Board import Board
from Wall import Direction


class Robot:
    def __init__(self, position: Tuple[int, int], color: str, robot_id: int):
        self.position = position
        self.color = color
        self.robot_id = robot_id

    def available_moves(self, board: Board):
        pass

    def move(
        self,
        direction: Direction,
        board_size: Tuple[int, int],
        other_positions: List[Tuple[int, int]],
        board: Board,
    ):
        moving = True
        while moving:
            x, y = self.position
            dx, dy = direction.value
            new_x, new_y = x + dx, y + dy

            # Check if the new position is within the board boundaries
            if 0 <= new_x < board_size[0] and 0 <= new_y < board_size[1]:

                # Check if new position is not another robot and not blocked by a wall
                if (new_x, new_y) not in other_positions and not board.is_wall(
                    self.position, (new_x, new_y)
                ):
                    self.position = (new_x, new_y)  # move the robot
                else:
                    moving = (
                        False  # Stop moving if another robot or a wall blocks the path
                    )
            else:
                moving = False  # Stop moving if the edge of the board is reached

        board.is_on_goal(self.position, self.robot_id)
