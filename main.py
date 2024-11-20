import chess
import tkinter as tk
from PIL import Image, ImageTk
import os


class ChessBoardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Satranç Tahtası")

        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack(side=tk.LEFT)

        # Taşlar
        self.piece_images = self.load_piece_images()
        self.pieces = {}  # Taşlar
        self.selected_piece = None  # Seçilen taş
        self.highlighted_squares = []  # Vurgulanan kareler
        self.valid_moves = []  # Geçerli hareketler

        # Hamleler
        self.moves_list = []  # Hamleler listesini burada saklayacağız

        # Satranç tahtasını oluştur
        self.board = chess.Board()
        self.create_board()

        # Fare olayları
        self.canvas.bind("<Button-1>", self.on_click)

        # Hamleler listesi paneli
        self.moves_panel = tk.Frame(self.root)
        self.moves_panel.pack(side=tk.LEFT, padx=20)
        self.moves_label = tk.Label(self.moves_panel, text="Hamleler", font=("Arial", 14))
        self.moves_label.pack()

        self.moves_text = tk.Text(self.moves_panel, width=30, height=10)
        self.moves_text.pack()

    def load_piece_images(self):
        pieces = ['P', 'R', 'N', 'B', 'Q', 'K']
        colors = ['w', 'b']
        images = {}
        for color in colors:
            for piece in pieces:
                piece_name = f"{color}{piece}.png"
                image_path = f"images/{piece_name}"

                if os.path.exists(image_path):
                    image = Image.open(image_path)
                    image = image.resize((50, 50))
                    images[f"{color}{piece}"] = ImageTk.PhotoImage(image)
                else:
                    print(f"Uyarı: {image_path} dosyası bulunamadı!")

        return images

    def create_board(self):
        """Tahtayı oluştur ve taşları yerleştir"""
        self.squares = {}
        colors = ["#f0d9b5", "#b58863"]  # Beyaz ve kahverengi zemin renkleri
        for row in range(8):
            for col in range(8):
                x1 = col * 50
                y1 = row * 50
                x2 = x1 + 50
                y2 = y1 + 50
                color = colors[(row + col) % 2]
                square = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                self.squares[(row, col)] = square

        self.place_pieces()

    def place_pieces(self):
        """Başlangıç taşlarını yerleştir"""
        for square in self.board.piece_map():
            piece = self.board.piece_at(square)
            if piece is not None:
                piece_name = self.get_piece_name(piece)
                row, col = divmod(square, 8)
                self.pieces[(row, col)] = self.canvas.create_image(col * 50 + 25, row * 50 + 25,
                                                                   image=self.piece_images[piece_name])

    def get_piece_name(self, piece):
        """Chess piece objesini taş ismine dönüştür"""
        color = 'w' if piece.color else 'b'
        piece_name = ''
        if piece.piece_type == chess.PAWN:
            piece_name = f"{color}P"
        elif piece.piece_type == chess.ROOK:
            piece_name = f"{color}R"
        elif piece.piece_type == chess.KNIGHT:
            piece_name = f"{color}N"
        elif piece.piece_type == chess.BISHOP:
            piece_name = f"{color}B"
        elif piece.piece_type == chess.QUEEN:
            piece_name = f"{color}Q"
        elif piece.piece_type == chess.KING:
            piece_name = f"{color}K"
        return piece_name

    def on_click(self, event):
        """Fare tıklama olayları"""
        x, y = event.x // 50, event.y // 50
        clicked_square = 8 * y + x  # Kareyi satranç tahtasında temsil eden sayıyı hesapla

        if self.selected_piece is None:
            # Seçilen taş var mı? Eğer varsa, seçilen taşı işaretle
            piece = self.board.piece_at(clicked_square)
            if piece is not None and (piece.color == self.board.turn):
                self.selected_piece = clicked_square
                self.highlight_moves(clicked_square)
        else:
            # Eğer bir taş seçildiyse, hareketi gerçekleştir
            self.make_move(self.selected_piece, clicked_square)
            self.selected_piece = None
            self.clear_highlighted_squares()

    def highlight_moves(self, square):
        """Geçerli taşın hareketlerini vurgulamak"""
        piece = self.board.piece_at(square)
        legal_moves = self.board.legal_moves
        self.valid_moves = [move for move in legal_moves if move.from_square == square]

        # Eski vurgulama karelerini temizle
        self.clear_highlighted_squares()

        for move in self.valid_moves:
            row, col = divmod(move.to_square, 8)
            self.highlighted_squares.append(self.canvas.create_oval(col * 50 + 10, row * 50 + 10,
                                                                    col * 50 + 40, row * 50 + 40,
                                                                    outline="red", width=2))

    def make_move(self, from_square, to_square):
        """Bir taşın hareketini yapmak"""
        move = chess.Move(from_square, to_square)
        if move in self.board.legal_moves:
            piece = self.board.piece_at(from_square)
            captured_piece = self.board.piece_at(to_square)

            # Hamleyi kaydet
            move_description = self.format_move(from_square, to_square, piece, captured_piece)
            self.moves_list.append(move_description)
            self.update_moves_panel()

            # Taşı yap
            self.board.push(move)
            self.update_board()

    def format_move(self, from_square, to_square, piece, captured_piece):
        """Hamleyi formatlamak"""
        from_row, from_col = divmod(from_square, 8)
        to_row, to_col = divmod(to_square, 8)

        piece_name = self.get_piece_name(piece)

        move_str = f"{self.get_color_name(piece.color)} {self.get_piece_type_name(piece)} {chr(from_col + 65)}{8 - from_row} -> {chr(to_col + 65)}{8 - to_row}"

        # Eğer taş yendi ise, bunu da belirt
        if captured_piece:
            captured_piece_name = self.get_piece_name(captured_piece)
            move_str += f" x {self.get_color_name(captured_piece.color)} {self.get_piece_type_name(captured_piece)}"

        return move_str

    def get_color_name(self, color):
        """Renk adı döndürür (Beyaz/Siyah)"""
        return "Beyaz" if color else "Siyah"

    def get_piece_type_name(self, piece):
        """Taş türünü isme dönüştürür (Piyon, Kale, vb.)"""
        if piece.piece_type == chess.PAWN:
            return "Piyon"
        elif piece.piece_type == chess.ROOK:
            return "Kale"
        elif piece.piece_type == chess.KNIGHT:
            return "At"
        elif piece.piece_type == chess.BISHOP:
            return "Fil"
        elif piece.piece_type == chess.QUEEN:
            return "Vezir"
        elif piece.piece_type == chess.KING:
            return "Şah"

    def update_moves_panel(self):
        """Hamleleri güncelle"""
        self.moves_text.delete(1.0, tk.END)
        for move in self.moves_list:
            self.moves_text.insert(tk.END, move + "\n")

    def update_board(self):
        """Tahtayı güncelle ve taşları yenile"""
        for square in self.pieces.values():
            self.canvas.delete(square)
        self.pieces.clear()

        # Yeni taşları yerleştir
        for square in self.board.piece_map():
            piece = self.board.piece_at(square)
            if piece is not None:
                piece_name = self.get_piece_name(piece)
                row, col = divmod(square, 8)
                self.pieces[(row, col)] = self.canvas.create_image(col * 50 + 25, row * 50 + 25,
                                                                   image=self.piece_images[piece_name])

    def clear_highlighted_squares(self):
        """Vurgulanan kareleri temizle"""
        for square in self.highlighted_squares:
            self.canvas.delete(square)
        self.highlighted_squares.clear()


# Uygulamayı başlat
root = tk.Tk()
app = ChessBoardApp(root)
root.mainloop()
