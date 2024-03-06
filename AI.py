from abc import ABC, abstractmethod
from AIInterface import AIInterface
from typing import List, Tuple


class State:
    """A state is a representation (=snapshot) of the game at a given point in time."""


class Action:
    """An action is a move that can be made in the game."""


class AI(ABC):
    """An AI is a class that can solve a game. It has to implement the following methods:"""

    def __init__(self, game_interface: AIInterface):
        super().__init__()
        self.game_interface = game_interface
        self.game_instance = game_interface.game_instance
        self.board = game_interface.game_instance.board

    @abstractmethod
    def actions(self, state: State) -> List[Action]:
        """Returns a list of all possible actions in the current state."""

    @abstractmethod
    def results(self, state: State, action) -> List[State]:
        """Returns the state after applying the action."""

    @abstractmethod
    def goal_test(self, state: State) -> bool:
        """Returns True if the state is a goal state, False otherwise."""

    @abstractmethod
    def path_cost(self, initial_state: State, action: Action, next_state: State) -> int:
        """Returns the cost of the path from the initial_state to the next_state."""

    @abstractmethod
    def solve(self, initial_state: State) -> List[Action]:
        """Returns a sequence of actions to solve the game."""
        pass
