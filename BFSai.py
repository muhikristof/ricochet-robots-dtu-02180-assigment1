from AIInterface import AIInterface


class BFSai:
    def __init__(self, game_interface: AIInterface):
        self.game_interface = game_interface

    def actions(self):
        pass

    def results(self):
        pass

    def goal_test(self):
        pass

    @staticmethod
    def solve(game_interface: AIInterface):
        ai = BFSai(game_interface)
