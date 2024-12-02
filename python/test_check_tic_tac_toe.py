import unittest
from check_tic_tac_toe import checkTicTacToeWin

class TestCheckTicTacToeWin(unittest.TestCase):
    def test_horizontal_win(self):
        board = [
            ['X', 'X', 'X'],
            ['O', 'O', ' '],
            [' ', ' ', ' ']
        ]
        self.assertEqual(checkTicTacToeWin(board), 'X')

    def test_vertical_win(self):
        board = [
            ['X', 'O', ' '],
            ['X', 'O', ' '],
            ['X', ' ', ' ']
        ]
        self.assertEqual(checkTicTacToeWin(board), 'X')

    def test_diagonal_win(self):
        board = [
            ['X', 'O', ' '],
            ['O', 'X', ' '],
            [' ', ' ', 'X']
        ]
        self.assertEqual(checkTicTacToeWin(board), 'X')

    def test_no_win(self):
        board = [
            ['X', 'O', 'X'],
            ['X', 'O', 'O'],
            ['O', 'X', 'X']
        ]
        self.assertEqual(checkTicTacToeWin(board), None)
    
    def test_undecided_game(self):
        board = [
            ['X', 'O', ' '],
            [' ', 'X', 'O'],
            ['O', ' ', ' ']
        ]
        self.assertEqual(checkTicTacToeWin(board), None)

if __name__ == '__main__':
    unittest.main()