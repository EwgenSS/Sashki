"""
Основной модуль игры в шашки, обрабатывающий пользовательский ввод и игровой цикл
"""

from board import Board
import re

class Game:
    """Класс для управления игровым процессом"""
    
    def __init__(self):
        """Инициализация новой игры"""
        self.board = Board()
        self.game_over = False
        self.winner = None
        self.ai_mode = False
    
    def start(self):
        """Запуск игрового цикла"""
        print("Добро пожаловать в консольную игру 'Шашки'!")
        print("Для хода введите координаты в формате: 'строка_откуда столбец_откуда строка_куда столбец_куда'")
        print("Например: '5 0 4 1'")
        print("Для выхода введите 'exit'")
        
        # Спрашиваем пользователя о режиме игры
        self.choose_game_mode()
        
        # Основной игровой цикл
        while not self.game_over:
            # Отображаем текущее состояние доски
            self.board.display()
            
            # Проверяем, завершена ли игра
            winner = self.board.get_winner()
            if winner is not None:
                self.game_over = True
                self.winner = winner
                break
            
            # Ход игрока или ИИ
            if self.ai_mode and self.board.current_player == self.board.WHITE:
                self.ai_move()
            else:
                self.player_move()
        
        # Отображаем результат игры
        self.board.display()
        if self.winner == self.board.BLACK:
            print("Игра окончена! Победили черные.")
        else:
            print("Игра окончена! Победили белые.")
    
    def choose_game_mode(self):
        """Выбор режима игры: против другого игрока или против ИИ"""
        while True:
            mode = input("Выберите режим игры (1 - против другого игрока, 2 - против ИИ): ")
            if mode == '1':
                self.ai_mode = False
                print("Выбран режим игры против другого игрока.")
                break
            elif mode == '2':
                self.ai_mode = True
                print("Выбран режим игры против ИИ. Вы играете черными.")
                break
            else:
                print("Некорректный ввод. Пожалуйста, введите 1 или 2.")
    
    def player_move(self):
        """Обработка хода игрока"""
        current_player = "черных" if self.board.current_player == self.board.BLACK else "белых"
        
        while True:
            move_input = input(f"Ход {current_player} (формат: строка_откуда столбец_откуда строка_куда столбец_куда): ")
            
            # Проверка на выход из игры
            if move_input.lower() == 'exit':
                print("Игра завершена пользователем.")
                self.game_over = True
                return
            
            # Проверка формата ввода
            if not re.match(r'^\d+ \d+ \d+ \d+$', move_input):
                print("Некорректный формат ввода. Используйте формат: 'строка_откуда столбец_откуда строка_куда столбец_куда'")
                continue
            
            # Разбор координат
            try:
                from_row, from_col, to_row, to_col = map(int, move_input.split())
                
                # Проверка координат на допустимость
                if not (0 <= from_row < 8 and 0 <= from_col < 8 and 0 <= to_row < 8 and 0 <= to_col < 8):
                    print("Координаты должны быть в диапазоне от 0 до 7.")
                    continue
                
                # Проверка, принадлежит ли шашка текущему игроку
                if not self.board.is_player_piece(from_row, from_col, self.board.current_player):
                    print("Вы можете перемещать только свои шашки.")
                    continue
                
                # Выполнение хода
                if self.board.make_move(from_row, from_col, to_row, to_col):
                    break
                else:
                    print("Недопустимый ход. Попробуйте снова.")
            
            except ValueError:
                print("Некорректный ввод. Используйте целые числа для координат.")
    
    def ai_move(self):
        """Выполнение хода ИИ"""
        print("ИИ думает...")
        
        # Получаем ход от ИИ
        from ai import AI
        ai = AI(self.board)
        from_row, from_col, to_row, to_col = ai.get_best_move()
        
        print(f"ИИ ходит: {from_row} {from_col} -> {to_row} {to_col}")
        
        # Выполняем ход
        self.board.make_move(from_row, from_col, to_row, to_col)

if __name__ == "__main__":
    game = Game()
    game.start()
