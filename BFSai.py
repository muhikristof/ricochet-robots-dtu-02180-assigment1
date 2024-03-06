from typing import List, Tuple, Optional, NamedTuple, NewType
from AIInterface import AIInterface
from Robot import AvailableMove
from Wall import Direction
import time


class RobotMove(NamedTuple):
    robot_id: int
    move: AvailableMove


RobotMoves = NewType("RobotMoves", List[RobotMove])
RobotsState = NewType("RobotsState", List[Tuple[int, int]])


class BFSai:
    def __init__(self, game_interface: AIInterface):
        self.game_interface = game_interface
        self.game_instance = game_interface.game_instance
        self.board = game_interface.game_instance.board
        self.robots_state: RobotsState = [
            robot.position for robot in self.game_instance.robots
        ]

    def actions(self, robots_state: RobotsState) -> RobotMoves:
        """Returns a list of all possible actions for the robots in the current state.

        Parameters:
        robots_state (RobotsState): The positions of the other robots.

        Returns:
        RobotMoves: A list of all possible actions for the robots in the current state.
        """
        available_actions: RobotMoves = []
        for robot in self.game_instance.robots:

            for move in robot.available_moves(
                self.game_interface.game_instance.board, robots_state
            ):
                available_actions.append(RobotMove(robot.robot_id, move))

        return available_actions

    def results(self, action: RobotMove) -> RobotsState:
        """Returns the state after applying the action.

        Parameters:
        action (RobotMove): The action to apply.

        Returns:
        RobotsState: The state after applying the action.
        """
        new_robots_state: RobotsState = self.robots_state.copy()
        new_robots_state[action.robot_id] = action.move.final_position
        return new_robots_state

    def goal_test(self):
        return [
            self.board.is_on_goal(robot.position, robot.robot_id)
            for robot in self.game_instance.robots
        ].count(True) == len(self.board.goals)

    def path_cost(self) -> float:
        return 1.0

    def solve(self) -> Optional[RobotMoves]:
        """Solves the game using BFS and returns the solution.

        Returns:
        Optional[RobotMoves]: The step-by-step solution to the game.
        """
        frontier: List[Tuple[RobotsState, RobotMoves]] = [
            (self.robots_state, RobotMoves([]))
        ]
        explored: List[RobotsState] = []

        while frontier:
            state, actions = frontier.pop(0)
            if self.goal_test():
                return actions

            explored.append(state)
            for action in self.actions(state):
                new_state = self.results(action)
                if new_state not in explored:
                    frontier.append((new_state, actions + RobotMoves([action])))

        return None

    @staticmethod
    def build_solution_and_play(game_interface: AIInterface):
        ai = BFSai(game_interface)

        solution = ai.solve()
        if solution is None:
            print("No solution found")
            return

        for robot_id, move in solution:
            new_position, on_goal = game_interface.move_robot(robot_id, move.direction)
            print(
                f"Moving robot {robot_id} -> {move.direction.name}, final position: {new_position}. On goal: {['No', 'Yes'][on_goal]}"
            )
            time.sleep(1)
