# ================================================================
# File: tictactoe/game.py
# Description:
#   The Game class manages the game flow and interactions between players.
#   - It initializes the board, handles turns, validates moves, and detects game outcomes.
#
# Steps Covered:
# 1. Clarify Requirements and Identify Core Use Cases.
# 4. Determine Core Methods Based on Use Cases.
# 6. Implement Necessary Methods.
# 7. Exception Handling and Edge Cases.
# ================================================================

from board import Board

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1  # Instance of Player
        self.player2 = player2  # Instance of Player
        self.board = Board()    # Instance of Board
        self.current_player = player1

    def play(self):
        # Print initial board state.
        self.board.print_board()

        # Continue the game until there is a winner or the board is full.
        while not self.board.is_full() and not self.board.has_winner():
            print(f"{self.current_player.get_name()}'s turn.")
            row = self.get_valid_input("Enter row (0-2): ")
            col = self.get_valid_input("Enter column (0-2): ")
            try:
                self.board.make_move(row, col, self.current_player.get_symbol())
                self.board.print_board()
                self.switch_player()
            except ValueError as e:
                print(str(e))

        # Determine and announce the result of the game.
        if self.board.has_winner():
            # When a win is detected, the last successful move was made by the previous player.
            self.switch_player()
            print(f"{self.current_player.get_name()} wins!")
        else:
            print("It's a draw!")

    def switch_player(self):
        # Switch between player1 and player2.
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def get_valid_input(self, message):
        # Continuously prompt for valid input.
        while True:
            try:
                user_input = int(input(message))
                if 0 <= user_input <= 2:
                    return user_input
                else:
                    print("Invalid input! Please enter a number between 0 and 2.")
            except ValueError:
                print("Invalid input! Please enter a number between 0 and 2.")
