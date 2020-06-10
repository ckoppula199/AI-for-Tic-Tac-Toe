"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    X always plays first. If even number of played tiles, then X's ai_turn
    else O's turn
    """
    O_count = 0
    X_count = 0
    for row in board:
        O_count += row.count("O")
        X_count += row.count("X")
    total = O_count + X_count

    if total % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    i, j = action
    # if tile has already been played then move is invalid
    if board[i][j] is not EMPTY:
        raise Exception
    board_copy = copy.deepcopy(board)
    current_player = player(board)
    board_copy[i][j] = current_player
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    X_won = winner_helper(board, X)
    if X_won:
        return X
    O_won = winner_helper(board, O)
    if O_won:
        return O
    return None


def winner_helper(board, current_player):

    if check_diagonal(board, current_player):
        return True

    for i in range(3):
        if check_vertical(board, current_player, i):
            return True

    for i in range(3):
        if check_horizontal(board, current_player, i):
            return True

    return False


def check_horizontal(board, current_player, row):
    if board[row][0] == board[row][1] == board[row][2] == current_player:
        return True
    return False


def check_vertical(board, current_player, col):
    if board[0][col] == board[1][col] == board[2][col] == current_player:
        return True
    return False


def check_diagonal(board, current_player):
    if board[0][0] == board[1][1] == board[2][2] == current_player:
        return True
    elif board[0][2] == board[1][1] == board[2][0] == current_player:
        return True
    return False


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    empty_count = 0

    for row in board:
        empty_count += row.count(EMPTY)

    if empty_count == 0:
        return True

    if winner(board) is not None:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    all_actions = actions(board)
    if player(board) == X:
        max_val = -math.inf
        best_move = set()
        for move in all_actions:
            val = min_value(result(board, move))
            if val > max_val:
                max_val = val
                best_move = move
        return best_move
    else:
        min_val = math.inf
        best_move = set()
        for move in all_actions:
            val = max_value(result(board, move))
            if val < min_val:
                min_val = val
                best_move = move
        return best_move


def max_value(board):
    """
    Recursivley calculates the max possible value of the board using min_value function
    """
    if terminal(board):
        return utility(board)

    max_value = -math.inf
    for action in actions(board):
        max_value = max(max_value, min_value(result(board, action)))

    return max_value


def min_value(board):
    """
    Recursively calculates the min possible value of the board using max_value function
    """
    if terminal(board):
        return utility(board)

    min_value = math.inf
    for action in actions(board):
        min_value = min(min_value, max_value(result(board, action)))

    return min_value
