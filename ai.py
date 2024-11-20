import chess
import random
from utils import evaluate_board

def minimax(board, depth, maximizing_player, alpha, beta):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, False, alpha, beta)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta Pruning
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, True, alpha, beta)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha Pruning
        return min_eval

def best_move(board):
    best_move = None
    max_eval = -float('inf')

    # Dinamik derinlik hesaplama
    depth = 3  # Başlangıç derinliği
    if board.fullmove_number > 20:  # Oyun ilerledikçe derinliği artırabiliriz
        depth = 4
    if board.fullmove_number > 40:  # İleri aşamalar için daha derin bir analiz
        depth = 5

    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth, False, -float('inf'), float('inf'))  # Alfa-Beta Pruning eklenmiş
        board.pop()
        if eval > max_eval:
            max_eval = eval
            best_move = move

    return best_move
