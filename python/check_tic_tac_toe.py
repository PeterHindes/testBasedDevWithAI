def checkTicTacToeWin(board):
    """
    Checks the given Tic Tac Toe board and returns the winner, if any.

    Args:
        board (list): A 3x3 list representing the Tic Tac Toe board.
            Each element in the list can be 'X', 'O', or ' ' (empty).

    Returns:
        str or None: The winner ('X' or 'O') if there is a winner, otherwise None.
    """
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]

    # Check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]

    # No winner
    return None
