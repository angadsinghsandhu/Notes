# ================================================================
# File: tictactoe/tictactoe_demo.py
# Description:
#   The TicTacToeDemo class acts as the entry point of the application.
#   - It creates instances of players and starts the game.
#
# Steps Covered:
# 1. Clarify Requirements and Identify Core Use Cases.
# 6. Implement Necessary Methods.
# 8. Follow Good Coding Practices.
# ================================================================

from game import Game
from player import Player

class TicTacToeDemo:
    @staticmethod
    def run():
        # Create two players with their respective symbols.
        player1 = Player("Player 1", 'X')
        player2 = Player("Player 2", 'O')
        # Initialize the game with the two players.
        game = Game(player1, player2)
        # Start the game.
        game.play()

if __name__ == "__main__":
    TicTacToeDemo.run()
