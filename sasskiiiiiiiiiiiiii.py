class Checkers:
    def __init__(self):
        self.board = self.create_board()
        self.current_player = 'w'  # Белые начинают

    def create_board(self):
        """Создаем начальную доску 8x8"""
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # Расставляем белые шашки (внизу)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'w'
        
        # Расставляем черные шашки (вверху)
        for row in range(0, 3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'b'
        return board

    def draw_board(self):
        """Отрисовываем текущее состояние доски"""
        print("\n  a b c d e f g h")
        for row_idx, row in enumerate(self.board):
            print(f"{8 - row_idx} ", end="")
            for col_idx, cell in enumerate(row):
                if (row_idx + col_idx) % 2 == 0:
                    print('■', end=" ")
                elif cell is None:
                    print('□', end=" ")
                else:
                    print('w' if cell == 'w' else 'b', end=" ")
            print(f" {8 - row_idx}")
        print("  a b c d e f g h\n")

    def parse_move(self, move_str):
        """Преобразуем ход из формата 'b6 c5' в координаты"""
        try:
            col_from = ord(move_str[0]) - ord('a')
            row_from = 8 - int(move_str[1])
            col_to = ord(move_str[3]) - ord('a')
            row_to = 8 - int(move_str[4])
            return (row_from, col_from), (row_to, col_to)
        except (IndexError, ValueError):
            return None, None

    def is_valid_move(self, from_pos, to_pos):
        """Проверяем, допустим ли ход"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Проверяем границы
        if not (0 <= from_row < 8 and 0 <= from_col < 8 and
                0 <= to_row < 8 and 0 <= to_col < 8):
            return False
        
        piece = self.board[from_row][from_col]
        
        # Проверяем, что двигаем свою шашку
        if piece != self.current_player:
            return False
        
        # Проверяем, что целевая клетка пуста
        if self.board[to_row][to_col] is not None:
            return False
        
        # Проверяем диагональное движение
        if piece == 'w':  # Белые ходят вверх
            if from_row - to_row != 1:
                return False
        else:  # Черные ходят вниз
            if to_row - from_row != 1:
                return False
        
        # Проверяем движение по диагонали
        if abs(from_col - to_col) != 1:
            return False
        
        # Проверяем, что ходим по темным клеткам
        if (from_row + from_col) % 2 == 0 or (to_row + to_col) % 2 == 0:
            return False
        
        return True

    def make_move(self, from_pos, to_pos):
        """Выполняем ход, если он допустим"""
        if not self.is_valid_move(from_pos, to_pos):
            return False
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Перемещаем шашку
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = None
        
        # Меняем игрока
        self.current_player = 'b' if self.current_player == 'w' else 'w'
        return True

    def play(self):
        """Основной игровой цикл"""
        print("Добро пожаловать в консольные шашки!")
        print("Ходы вводятся в формате: 'b6 c5' (столбец-строка столбец-строка)")
        print("Пример: a2 b3 - перемещение шашки с a2 на b3")
        
        while True:
            self.draw_board()
            print(f"Ход {'белых' if self.current_player == 'w' else 'черных'}")
            move = input("Ваш ход (или 'выход' для завершения): ")
            
            if move.lower() == 'выход':
                print("Игра завершена!")
                break
            
            from_pos, to_pos = self.parse_move(move)
            if from_pos is None or to_pos is None:
                print("Некорректный ввод! Используйте формат: 'b6 c5'")
                continue
            
            if self.make_move(from_pos, to_pos):
                print("Ход выполнен!")
            else:
                print("Недопустимый ход! Попробуйте снова.")

# Запуск игры
if __name__ == "__main__":
    game = Checkers()
    game.play()

