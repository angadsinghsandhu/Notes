# ================================================================
# File: tictactoe/player.py
# Description:
#   The Player class represents a player in the game.
#   - It holds the player's name and symbol (either 'X' or 'O').
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# ================================================================

class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def get_name(self):
        return self.name

    def get_symbol(self):
        return self.symbol
