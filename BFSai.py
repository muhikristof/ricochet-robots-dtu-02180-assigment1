from typing import List, Tuple, Optional, NamedTuple, NewType
from AI import AI
from AIInterface import AIInterface
from Robot import Robot, AvailableMove
from Wall import Direction
from collections import deque
import time


class RobotMove(NamedTuple):
    robot_id: int
    move: AvailableMove


RobotMoves = NewType("RobotMoves", List[RobotMove])
RobotsState = NewType("RobotsState", List[Tuple[int, int]])


class BFSai(AI):
    def actions(self, robots_state: RobotsState) -> RobotMoves:
        """Returns a list of all possible actions for the robots in the current state.

        Parameters:
        robots_state (RobotsState): The positions of all robots.

        Returns:
        RobotMoves: A list of all possible actions for the robots in the current state.
        """
        available_actions: RobotMoves = []
        for robot_id, robot_pos in enumerate(robots_state):
            other_robots_positions = [
                pos for i, pos in enumerate(robots_state) if i != robot_id
            ]

            for move in Robot.available_moves(
                robot_pos,
                self.game_interface.game_instance.board,
                other_robots_positions,
            ):
                available_actions.append(RobotMove(robot_id, move))

        return available_actions

    def results(self, robots_state: RobotsState, action: RobotMove) -> RobotsState:
        """Returns the state after applying the action.

        Parameters:
        robots_state (RobotsState): The current state of the robots.
        action (RobotMove): The action to apply.

        Returns:
        RobotsState: The state after applying the action.
        """
        new_robots_state: RobotsState = robots_state.copy()
        new_robots_state[action.robot_id] = action.move.final_position
        return new_robots_state

    def goal_test(self, robots_state: RobotsState) -> bool:
        """Returns True if all robots are on a goal, False otherwise."""
        return [
            self.board.is_on_goal(pos, i) for i, pos in enumerate(robots_state)
        ].count(True) == len(self.board.goals)

    def path_cost(self) -> int:
        return 1

    def solve(self, initial_state: RobotsState) -> Optional[RobotMoves]:
        """Solves the game using BFS and returns the solution.

        Returns:
        Optional[RobotMoves]: The step-by-step solution to the game.
        """
        # Define a queue for BFS. Each element is a tuple (robots_state, path).
        queue: deque[Tuple[RobotsState, RobotMoves]] = deque(
            [(initial_state, RobotMoves([]))]
        )

        # Set to keep track of visited states to avoid cycles.
        visited = set([tuple(initial_state)])

        while queue:
            current_state, path = queue.popleft()

            # Draw updated positions (debugging purposes only)
            # for i, pos in enumerate(current_state):
            #     self.game_instance.robots[i].position = pos
            #     self.game_instance.update_board()
            #     self.game_instance.master.update_idletasks()

            if self.goal_test(current_state):
                return path  # Found the solution

            for action in self.actions(current_state):
                new_state = self.results(current_state, action)

                # Prevent revisiting already visited states.
                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))
                    queue.append((new_state, RobotMoves(path + [action])))

        # If the queue is empty and no solution was found
        return None

    @staticmethod
    def build_solution_and_play(game_interface: AIInterface):
        ai = BFSai(game_interface)
        initial_state = RobotsState(
            [robot.position for robot in game_interface.game_instance.robots]
        )

        solution = ai.solve(initial_state)
        if solution is None:
            print("No solution found")
            return

        print(f"Found a solution with {len(solution)} steps")

        for robot_id, move in solution:
            new_position, on_goal = game_interface.move_robot(robot_id, move.direction)
            print(
                f"Moving robot {robot_id} -> {move.direction.name}, final position: {new_position}. On goal: {['No', 'Yes'][on_goal]}"
            )
            time.sleep(1)
