from typing import List, Tuple, Optional, NamedTuple, NewType
from AI import AI
from AIInterface import AIInterface
from Robot import Robot, AvailableMove
from Wall import Direction
from collections import deque
from heapq import heappop, heappush
import time


class RobotMove(NamedTuple):
    robot_id: int
    move: AvailableMove


RobotMoves = NewType("RobotMoves", List[RobotMove])
RobotsState = NewType("RobotsState", List[Tuple[int, int]])


class GraphSearchAI(AI):
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

    def heuristic(self, robots_state: RobotsState) -> int:
        """
        Calculates the heuristic cost of a given state.

        Parameters:
        robots_state (RobotsState): The current state of the robots.

        Returns:
        int: The heuristic cost estimate to reach the goal from the current state.
        """
        total_distance = 0
        for robot_position in robots_state:
            # Assuming the Goal class has 'x' and 'y' attributes for its position
            distances = [abs(robot_position[0] - goal.x) + abs(robot_position[1] - goal.y)
                         for goal in self.board.goals]
            total_distance += min(distances)
        return total_distance

    def solve_a_star(self, initial_state: RobotsState) -> Optional[RobotMoves]:
        """
        Solves the game using the A* and returns the solution.

        Parameters:
        initial_state (RobotsState): The initial state of the game.

        Returns:
        Optional[RobotMoves]: The step-by-step solution to the game.
        """
        start_time = time.time()
        # Priority queue for A*, storing elements as tuples (priority, (state, path))
        frontier = [(0, (initial_state, RobotMoves([])))]
        visited = set([tuple(initial_state)])
        moves_tried = 0

        while frontier:
            priority, (current_state, path) = heappop(frontier)

            if self.goal_test(current_state):
                end_time = time.time()
                print(f"Solution found in {end_time - start_time:.2f} seconds with total moves tried: {moves_tried}")
                return path

            for action in self.actions(current_state):
                new_state = self.results(current_state, action)
                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))
                    cost_so_far = len(path) + 1  # Each move has a cost of 1
                    priority = cost_so_far + self.heuristic(new_state)
                    heappush(frontier, (priority, (new_state, RobotMoves(path + [action]))))
                    moves_tried += 1

        end_time = time.time()
        print(f"Search concluded in {end_time - start_time:.2f} seconds with no solution found.")
        return None

    def solve_bfs(self, initial_state: RobotsState) -> Optional[RobotMoves]:
        """Solves the game using BFS and returns the solution.

        Returns:
        Optional[RobotMoves]: The step-by-step solution to the game.
        """
        start_time = time.time()  # start the time

        # Define a queue for BFS. Each element is a tuple (robots_state, path).
        queue: deque[Tuple[RobotsState, RobotMoves]] = deque(
            [(initial_state, RobotMoves([]))]
        )
        moves_tried = 0  # Initialize counter for moves tried

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
                end_time = time.time()  # Record the end time when the solution is found
                print(
                    f"Solution found in {end_time - start_time:.2f} seconds with total moves tried: {moves_tried}"
                )
                return path  # Found the solution

            for action in self.actions(current_state):
                new_state = self.results(current_state, action)

                # Prevent revisiting already visited states.
                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))
                    queue.append((new_state, RobotMoves(path + [action])))
                    moves_tried += 1

        # If the queue is empty and no solution was found
        end_time = time.time()  # Stop timer if no solution
        return None

    def solve_dfs(self, initial_state: RobotsState) -> Optional[RobotMoves]:
        """Solves the game using DFS and returns the solution.

        Parameters:
        initial_state (RobotsState): The initial state of the game.

        Returns:
        Optional[RobotMoves]: The step-by-step solution to the game.
        """
        start_time = time.time()
        stack = [(initial_state, RobotMoves([]))]
        visited = set([tuple(initial_state)])
        moves_tried = 0

        while stack:
            current_state, path = stack.pop()

            if self.goal_test(current_state):
                end_time = time.time()
                print(
                    f"Solution found in {end_time - start_time:.2f} seconds with total moves tried: {moves_tried}"
                )
                return path

            for action in self.actions(current_state):
                new_state = self.results(current_state, action)

                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))
                    stack.append((new_state, RobotMoves(path + [action])))
                    moves_tried += 1

        end_time = time.time()
        return None

    def solve(
        self, initial_state: RobotsState, ai_type: str = "bfs"
    ) -> Optional[RobotMoves]:
        """Solves the game using either BFS or DFS and returns the solution.

        Parameters:
        initial_state (RobotsState): The initial state of the game.
        bfs (bool): If True, uses BFS. Otherwise, uses DFS.

        Returns:
        Optional[RobotMoves]: The step-by-step solution to the game.
        """
        print("solving with: " + ai_type)
        if ai_type == 'bfs':
            return self.solve_bfs(initial_state)
        elif ai_type == 'dfs':
            return self.solve_dfs(initial_state)
        elif ai_type == 'a_star':
            return self.solve_a_star(initial_state)

    @staticmethod
    def build_solution_and_play(game_interface: AIInterface, ai_type: str = "bfs"):
        """ """
        ai = GraphSearchAI(game_interface)
        initial_state = RobotsState(
            [robot.position for robot in game_interface.game_instance.robots]
        )

        solution = ai.solve(initial_state, ai_type)

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
