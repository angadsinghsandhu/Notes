# Tic Tac Toe Game

## Key Points and SOLID Application:

### Single Responsibility:
Each class is responsible for a distinct part of the system (e.g., Board handles grid operations, Player encapsulates player data, and Game controls the game flow).

### Open/Closed:
The classes are open for extension (for example, you could extend the game to support different board sizes) but closed for modification.

### Liskov Substitution:
Derived or alternative implementations (if any) could replace the classes without breaking the game logic.

### Interface Segregation:
Each class exposes only the methods that are necessary for its clients.

### Dependency Inversion:
The high-level module (Game) depends on abstractions (e.g., the Player interface) rather than on concrete implementations.

## Directory Structure

```text
tictactoe/
├── board.py
├── game.py
├── player.py
└── tictactoe_demo.py
```

## Summary of Design Steps and SOLID Application

1. **Clarify Requirements and Identify Core Use Cases:**
   - The game is played on a 3x3 grid.
   - Two players take turns placing their symbols.
   - The game detects wins (three in a row) and draws.

2. **Identify Key Entities:**
   - **Player:** Represents a game participant.
   - **Board:** Manages the grid and validates moves.
   - **Game:** Orchestrates the gameplay and player interactions.

3. **Define Classes and Their Attributes:**
   - `Player` holds player name and symbol.
   - `Board` maintains the grid and count of moves.
   - `Game` maintains the game state including the current player and board.

4. **Determine Core Methods Based on Use Cases:**
   - `Board.make_move()`, `Board.is_full()`, `Board.has_winner()`, and `Board.print_board()`.
   - `Game.play()`, `Game.switch_player()`, and `Game.get_valid_input()`.

5. **Define Relationships Between Classes:**
   - **Composition:** `Game` composes a `Board` and two `Player` instances.
   - **Interaction:** `Game` interacts with `Board` and `Player` objects to manage gameplay.

6. **Implement Necessary Methods:**
   - Each class implements methods to manage its responsibilities, e.g., `Board` handles grid operations, and `Game` controls the turn-based logic.

7. **Exception Handling and Edge Cases:**
   - The `Board.make_move()` method raises a `ValueError` for invalid moves.
   - The `Game.get_valid_input()` method ensures only valid input is accepted.

8. **Follow Good Coding Practices:**
   - Clear and meaningful naming for classes and methods.
   - Separation of concerns with each class handling its own responsibilities.
   - Modular design allowing easy maintenance and extension.