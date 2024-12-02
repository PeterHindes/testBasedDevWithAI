def checkTicTacToeWin(board):
    """
    Check if there's a winner in a Tic-tac-toe game.
    
    Args:
        board (list): A 3x3 list representing the Tic-tac-toe board.
                     Contains 'X', 'O', or ' ' (empty space)
    
    Returns:
        str or None: Returns 'X' or 'O' if there's a winner, None if no winner
    """
    
    # Check horizontal wins
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]
    
    # Check vertical wins
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]
    
    # Check diagonal wins
    # Main diagonal (top-left to bottom-right)
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    
    # Secondary diagonal (top-right to bottom-left)
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    
    # If no winner is found
    return None
