# Chess-Engine

This is a Python implementation of the classic game of Chess. It allows two players to play against each other.

## Features

- Move validation: The game enforces the rules of chess, ensuring that players can only make legal moves.
- Checkmate detection: The game detects when a player's king is in checkmate, resulting in the end of the game.
- Castling: Players can perform the castling move, a special move in chess that involves the king and a rook.
- Promotion: When a pawn reaches the opposite end of the board, it can be promoted to a more powerful piece (Currently Queen).

## Getting Started

1. Clone the repository: `git clone https://github.com/sainikhils02/chess-game.git`
2. Navigate to the project directory: `cd chess-game`
3. Run the game: `python chessMain.py`

## How to Play

1. The game starts with the white player making the first move.
2. Players take turns entering clicking their moves from the beginning_square to end_square.
3. The game will validate the move and update the board accordingly.
4. Continue taking turns until one player achieves checkmate or the game ends in a draw.

