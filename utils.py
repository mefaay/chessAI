import chess


# Bu fonksiyon her taşın temel değerini hesaplar.
def piece_value(piece):
    values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 1000
    }
    return values.get(piece.piece_type, 0)


# Bu fonksiyon, taşların konumlarına göre değer ekler.
def piece_value_with_position(piece, square, board):
    base_value = piece_value(piece)  # Taşın temel değeri
    position_value = 0

    # Piyon pozisyonel değeri (merkeze yakın olmak daha iyi)
    if piece.piece_type == chess.PAWN:
        if piece.color == chess.WHITE:
            position_value = 0.1 * (6 - chess.square_rank(square))  # Piyonlar üst sıralara çıktıkça değer kazanır
        else:
            position_value = 0.1 * chess.square_rank(square)  # Siyah piyonlar yukarıda değer kazanır

    # Atlar ve fillerin pozisyonel değeri
    if piece.piece_type == chess.KNIGHT:
        position_value = knight_position_value(piece.color, square)

    if piece.piece_type == chess.BISHOP:
        position_value = bishop_position_value(piece.color, square, board)

    return base_value + position_value


def knight_position_value(color, square):
    # Atlar merkezde daha güçlüdür
    if color == chess.WHITE:
        return 0.5 * (4 - abs(3 - chess.square_rank(square)))  # Merkeze yakın olmak daha iyi
    else:
        return 0.5 * abs(3 - chess.square_rank(square))


def bishop_position_value(color, square, board):
    # Beyaz veya siyah filin tahtadaki pozisyonuna göre
    if color == chess.WHITE:
        return 0.2 * (6 - chess.square_rank(square))  # Yukarıda daha iyi
    else:
        return 0.2 * chess.square_rank(square)


# Bu fonksiyon tahtadaki taşları değerlendirir.
def evaluate_board(board):
    evaluation = 0

    # Pozisyonel Değerleme (Taşların pozisyonlarını hesaba kat)
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            piece_value = piece_value_with_position(piece, square, board)
            if piece.color == chess.WHITE:
                evaluation += piece_value
            else:
                evaluation -= piece_value

    # Kralın güvenliğini de dikkate al
    evaluation += evaluate_king_safety(board)

    return evaluation


def evaluate_king_safety(board):
    # Kralların güvenliğini değerlendir
    evaluation = 0
    white_king = board.king(chess.WHITE)
    black_king = board.king(chess.BLACK)

    # Beyaz ve siyah kralların etrafındaki taşları göz önünde bulundur
    if white_king is not None:
        evaluation -= sum(1 for sq in chess.SQUARES if board.piece_at(sq) and board.piece_at(sq).color == chess.BLACK)

    if black_king is not None:
        evaluation += sum(1 for sq in chess.SQUARES if board.piece_at(sq) and board.piece_at(sq).color == chess.WHITE)

    return evaluation
