"""
Модуль для представления игровой доски и основных функций шашек
"""

class Board:
    """Класс для представления игровой доски в шашках"""
    
    # Константы для представления клеток доски
    EMPTY = 0
    WHITE = 1
    BLACK = 2
    WHITE_KING = 3
    BLACK_KING = 4
    
    # Символы для отображения в консоли
    SYMBOLS = {
        EMPTY: ' ',
        WHITE: '○',
        BLACK: '●',
        WHITE_KING: '♔',
        BLACK_KING: '♚'
    }
    
    def __init__(self):
        """Инициализация новой доски для игры в шашки"""
        # Создаем доску 8x8
        self.board = [[self.EMPTY for _ in range(8)] for _ in range(8)]
        self.setup_board()
        self.current_player = self.BLACK  # Черные ходят первыми
        self.white_count = 12
        self.black_count = 12
        
    def setup_board(self):
        """Расстановка начальной позиции шашек на доске"""
        # Расставляем белые шашки (нижняя часть доски)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:  # Только на черных клетках
                    self.board[row][col] = self.WHITE
        
        # Расставляем черные шашки (верхняя часть доски)
        for row in range(0, 3):
            for col in range(8):
                if (row + col) % 2 == 1:  # Только на черных клетках
                    self.board[row][col] = self.BLACK
    
    def display(self):
        """Отображение текущего состояния доски в консоли"""
        print("  0 1 2 3 4 5 6 7")  # Номера столбцов
        print(" +-----------------+")
        
        for row in range(8):
            print(f"{row}|", end="")  # Номер строки
            for col in range(8):
                piece = self.board[row][col]
                # Добавляем цветовое оформление для клеток доски
                if (row + col) % 2 == 0:  # Белые клетки
                    print(f"\033[47m {self.SYMBOLS[piece]} \033[0m", end="")
                else:  # Черные клетки
                    print(f"\033[40m {self.SYMBOLS[piece]} \033[0m", end="")
            print("|")
            
        print(" +-----------------+")
        print(f"Ход {'черных' if self.current_player == self.BLACK else 'белых'}")
        print(f"Белых шашек: {self.white_count}, Черных шашек: {self.black_count}")
    
    def is_valid_position(self, row, col):
        """Проверка, находится ли позиция в пределах доски"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def is_empty(self, row, col):
        """Проверка, пуста ли клетка"""
        return self.board[row][col] == self.EMPTY
    
    def get_piece(self, row, col):
        """Получение шашки на указанной позиции"""
        return self.board[row][col]
    
    def is_player_piece(self, row, col, player):
        """Проверка, принадлежит ли шашка указанному игроку"""
        piece = self.board[row][col]
        if player == self.WHITE:
            return piece == self.WHITE or piece == self.WHITE_KING
        else:
            return piece == self.BLACK or piece == self.BLACK_KING
    
    def is_king(self, row, col):
        """Проверка, является ли шашка дамкой"""
        piece = self.board[row][col]
        return piece == self.WHITE_KING or piece == self.BLACK_KING
    
    def make_king(self, row, col):
        """Превращение шашки в дамку"""
        piece = self.board[row][col]
        if piece == self.WHITE:
            self.board[row][col] = self.WHITE_KING
        elif piece == self.BLACK:
            self.board[row][col] = self.BLACK_KING
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        """Перемещение шашки с одной позиции на другую"""
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = self.EMPTY
        
        # Проверка на превращение в дамку
        if (to_row == 0 and self.board[to_row][to_col] == self.WHITE) or \
           (to_row == 7 and self.board[to_row][to_col] == self.BLACK):
            self.make_king(to_row, to_col)
    
    def remove_piece(self, row, col):
        """Удаление шашки с доски"""
        piece = self.board[row][col]
        self.board[row][col] = self.EMPTY
        
        # Обновляем счетчики шашек
        if piece == self.WHITE or piece == self.WHITE_KING:
            self.white_count -= 1
        elif piece == self.BLACK or piece == self.BLACK_KING:
            self.black_count -= 1
    
    def switch_player(self):
        """Переключение текущего игрока"""
        self.current_player = self.BLACK if self.current_player == self.WHITE else self.WHITE
    
    def get_winner(self):
        """Определение победителя, если игра завершена"""
        if self.white_count == 0:
            return self.BLACK
        elif self.black_count == 0:
            return self.WHITE
        
        # Проверка на отсутствие возможных ходов
        if not self.get_all_possible_moves(self.current_player):
            return self.BLACK if self.current_player == self.WHITE else self.WHITE
        
        return None  # Игра продолжается
    
    def get_all_possible_moves(self, player):
        """Получение всех возможных ходов для указанного игрока"""
        moves = []
        captures = []  # Отдельный список для ходов с взятием
        
        for row in range(8):
            for col in range(8):
                if self.is_player_piece(row, col, player):
                    # Получаем возможные ходы для текущей шашки
                    piece_moves = self.get_piece_moves(row, col)
                    piece_captures = self.get_piece_captures(row, col)
                    
                    moves.extend(piece_moves)
                    captures.extend(piece_captures)
        
        # Если есть ходы с взятием, возвращаем только их (обязательное взятие)
        if captures:
            return captures
        return moves
    
    def get_piece_moves(self, row, col):
        """Получение возможных ходов для шашки без взятия"""
        moves = []
        piece = self.board[row][col]
        
        # Определяем направления движения в зависимости от типа шашки
        directions = []
        if piece == self.WHITE or piece == self.WHITE_KING:
            directions.extend([(-1, -1), (-1, 1)])  # Белые двигаются вверх
        if piece == self.BLACK or piece == self.BLACK_KING:
            directions.extend([(1, -1), (1, 1)])    # Черные двигаются вниз
        
        # Дамки могут двигаться в любом направлении на любое расстояние
        if self.is_king(row, col):
            for dr, dc in directions:
                r, c = row + dr, col + dc
                while self.is_valid_position(r, c) and self.is_empty(r, c):
                    moves.append((row, col, r, c))
                    r += dr
                    c += dc
        else:
            # Обычные шашки двигаются на одну клетку
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if self.is_valid_position(r, c) and self.is_empty(r, c):
                    moves.append((row, col, r, c))
        
        return moves
    
    def get_piece_captures(self, row, col):
        """Получение возможных ходов с взятием для шашки"""
        captures = []
        piece = self.board[row][col]
        player = self.WHITE if piece == self.WHITE or piece == self.WHITE_KING else self.BLACK
        opponent = self.BLACK if player == self.WHITE else self.WHITE
        
        # Все возможные направления для взятия
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        # Для обычных шашек ограничиваем направления
        if not self.is_king(row, col):
            if player == self.WHITE:
                directions = [(-1, -1), (-1, 1)]  # Белые двигаются вверх
            else:
                directions = [(1, -1), (1, 1)]    # Черные двигаются вниз
        
        # Проверяем возможность взятия в каждом направлении
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if self.is_valid_position(r, c) and not self.is_empty(r, c) and not self.is_player_piece(r, c, player):
                # Проверяем, свободна ли клетка за шашкой противника
                next_r, next_c = r + dr, c + dc
                if self.is_valid_position(next_r, next_c) and self.is_empty(next_r, next_c):
                    captures.append((row, col, next_r, next_c, r, c))  # Добавляем координаты взятой шашки
        
        return captures
    
    def make_move(self, from_row, from_col, to_row, to_col):
        """Выполнение хода с проверкой правил"""
        # Получаем все возможные ходы для текущего игрока
        possible_moves = self.get_all_possible_moves(self.current_player)
        
        # Проверяем, является ли ход допустимым
        for move in possible_moves:
            if len(move) == 4:  # Обычный ход
                if move == (from_row, from_col, to_row, to_col):
                    self.move_piece(from_row, from_col, to_row, to_col)
                    self.switch_player()
                    return True
            elif len(move) == 6:  # Ход с взятием
                if move[:4] == (from_row, from_col, to_row, to_col):
                    # Выполняем ход и удаляем взятую шашку
                    self.move_piece(from_row, from_col, to_row, to_col)
                    self.remove_piece(move[4], move[5])
                    
                    # Проверяем, может ли шашка продолжить взятие
                    additional_captures = self.get_piece_captures(to_row, to_col)
                    if not additional_captures:
                        self.switch_player()
                    
                    return True
        
        return False  # Недопустимый ход
    
    def clone(self):
        """Создание копии текущего состояния доски"""
        new_board = Board()
        new_board.board = [row[:] for row in self.board]
        new_board.current_player = self.current_player
        new_board.white_count = self.white_count
        new_board.black_count = self.black_count
        return new_board
