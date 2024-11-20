import chess


class ChessBoard:
    def __init__(self):
        self.board = chess.Board()

    def print_board(self):
        print(self.board)

    def get_move(self, move_str):
        # Move'yu UCI formatından bir hareket objesine dönüştürür
        return chess.Move.from_uci(move_str)

    def apply_move(self, move_str):
        # Move'yu tahtaya uygular
        move = self.get_move(move_str)
        if move in self.board.legal_moves:
            self.board.push(move)
            print(f"Geçerli hamle: {move}")
            self.print_board()
        else:
            print("Geçersiz hamle.")


# Test amaçlı basit bir örnek
if __name__ == "__main__":
    game = ChessBoard()
    game.print_board()

    move = "e2e4"  # Örneğin "e2e4" hamlesini alalım
    print(f"\nHamle: {move}")
    game.apply_move(move)  # Hamleyi uygula

    # Geçersiz bir hamleyi test et
    invalid_move = "e2e5"  # Geçersiz bir hamle örneği
    print(f"\nHamle: {invalid_move}")
    game.apply_move(invalid_move)  # Geçersiz hamleyi uygula
