from typing import List, Tuple, Optional
from AIInterface import AIInterface
from Wall import Direction
import time


class BFSai:
    def __init__(self, game_interface: AIInterface):
        self.game_interface = game_interface

    def actions(self):
        pass

    def results(self):
        pass

    def goal_test(self):
        pass

    def path_cost(self) -> float:
        return 1.0

    def solve(self) -> Optional[List[Tuple[int, Direction]]]:
        pass

    @staticmethod
    def build_solution_and_play(game_interface: AIInterface):
        ai = BFSai(game_interface)

        solution = ai.solve()
        if solution is None:
            print("No solution found")
            return

        for robot_id, direction in solution:
            new_position, on_goal = game_interface.move_robot(robot_id, direction)
            print(
                f"Moving robot {robot_id} -> {direction.name}, final position: {new_position}. On goal: {['No', 'Yes'][on_goal]}"
            )
            time.sleep(1)
