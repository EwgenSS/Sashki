"""
Модуль искусственного интеллекта для игры в шашки
"""

import random
import time
from copy import deepcopy

class AI:
    """Класс для реализации искусственного интеллекта в игре шашки"""
    
    def __init__(self, board, difficulty=2):
        """
        Инициализация ИИ
        
        Args:
            board: Текущее состояние игровой доски
            difficulty: Уровень сложности ИИ (1-3)
        """
        self.board = board
        self.difficulty = difficulty
        self.max_depth = self.difficulty * 2  # Глубина поиска зависит от сложности
        self.player = board.WHITE  # ИИ всегда играет за белых
    
    def get_best_move(self):
        """
        Определение лучшего хода для ИИ
        
        Returns:
            tuple: Координаты лучшего хода (from_row, from_col, to_row, to_col)
        """
        # Добавляем небольшую задержку для имитации "размышления"
        time.sleep(1)
        
        # Получаем все возможные ходы
        possible_moves = self.board.get_all_possible_moves(self.player)
        
        if not possible_moves:
            return None  # Нет доступных ходов
        
        # Для низкого уровня сложности выбираем случайный ход
        if self.difficulty == 1:
            return self._choose_random_move(possible_moves)
        
        # Для средней и высокой сложности используем минимакс с разной глубиной
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        for move in possible_moves:
            # Создаем копию доски для симуляции хода
            board_copy = self.board.clone()
            
            # Выполняем ход
            if len(move) == 4:  # Обычный ход
                from_row, from_col, to_row, to_col = move
                board_copy.move_piece(from_row, from_col, to_row, to_col)
                board_copy.switch_player()
            else:  # Ход с взятием
                from_row, from_col, to_row, to_col, capture_row, capture_col = move
                board_copy.move_piece(from_row, from_col, to_row, to_col)
                board_copy.remove_piece(capture_row, capture_col)
                
                # Проверяем, может ли шашка продолжить взятие
                additional_captures = board_copy.get_piece_captures(to_row, to_col)
                if not additional_captures:
                    board_copy.switch_player()
            
            # Оцениваем ход с помощью минимакса
            value = self._minimax(board_copy, self.max_depth - 1, False, alpha, beta)
            
            if value > best_value:
                best_value = value
                best_move = (from_row, from_col, to_row, to_col)
            
            alpha = max(alpha, best_value)
        
        # Если не нашли хороший ход, выбираем случайный
        if best_move is None:
            return self._choose_random_move(possible_moves)
        
        return best_move
    
    def _choose_random_move(self, moves):
        """Выбор случайного хода из списка возможных"""
        move = random.choice(moves)
        if len(move) == 4:  # Обычный ход
            return move
        else:  # Ход с взятием
            return move[:4]  # Возвращаем только координаты хода без координат взятой шашки
    
    def _minimax(self, board, depth, is_maximizing, alpha, beta):
        """
        Алгоритм минимакс с альфа-бета отсечением для оценки ходов
        
        Args:
            board: Текущее состояние доски
            depth: Текущая глубина поиска
            is_maximizing: True, если текущий ход максимизирующего игрока (ИИ)
            alpha: Альфа значение для отсечения
            beta: Бета значение для отсечения
            
        Returns:
            float: Оценка позиции
        """
        # Базовый случай: достигнута максимальная глубина или игра окончена
        winner = board.get_winner()
        if depth == 0 or winner is not None:
            return self._evaluate_board(board)
        
        current_player = self.player if is_maximizing else board.BLACK
        possible_moves = board.get_all_possible_moves(current_player)
        
        # Если нет ходов, позиция проигрышная
        if not possible_moves:
            return float('-inf') if is_maximizing else float('inf')
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in possible_moves:
                # Создаем копию доски для симуляции хода
                board_copy = board.clone()
                
                # Выполняем ход
                if len(move) == 4:  # Обычный ход
                    from_row, from_col, to_row, to_col = move
                    board_copy.move_piece(from_row, from_col, to_row, to_col)
                    board_copy.switch_player()
                else:  # Ход с взятием
                    from_row, from_col, to_row, to_col, capture_row, capture_col = move
                    board_copy.move_piece(from_row, from_col, to_row, to_col)
                    board_copy.remove_piece(capture_row, capture_col)
                    
                    # Проверяем, может ли шашка продолжить взятие
                    additional_captures = board_copy.get_piece_captures(to_row, to_col)
                    if not additional_captures:
                        board_copy.switch_player()
                
                # Рекурсивно оцениваем позицию
                eval_value = self._minimax(board_copy, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval_value)
                
                # Альфа-бета отсечение
                alpha = max(alpha, eval_value)
                if beta <= alpha:
                    break
                
            return max_eval
        else:
            min_eval = float('inf')
            for move in possible_moves:
                # Создаем копию доски для симуляции хода
                board_copy = board.clone()
                
                # Выполняем ход
                if len(move) == 4:  # Обычный ход
                    from_row, from_col, to_row, to_col = move
                    board_copy.move_piece(from_row, from_col, to_row, to_col)
                    board_copy.switch_player()
                else:  # Ход с взятием
                    from_row, from_col, to_row, to_col, capture_row, capture_col = move
                    board_copy.move_piece(from_row, from_col, to_row, to_col)
                    board_copy.remove_piece(capture_row, capture_col)
                    
                    # Проверяем, может ли шашка продолжить взятие
                    additional_captures = board_copy.get_piece_captures(to_row, to_col)
                    if not additional_captures:
                        board_copy.switch_player()
                
                # Рекурсивно оцениваем позицию
                eval_value = self._minimax(board_copy, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval_value)
                
                # Альфа-бета отсечение
                beta = min(beta, eval_value)
                if beta <= alpha:
                    break
                
            return min_eval
    
    def _evaluate_board(self, board):
        """
        Оценка текущей позиции на доске
        
        Args:
            board: Текущее состояние доски
            
        Returns:
            float: Числовая оценка позиции (больше - лучше для ИИ)
        """
        # Проверяем, есть ли победитель
        winner = board.get_winner()
        if winner == self.player:
            return 1000  # Выигрышная позиция для ИИ
        elif winner is not None:
            return -1000  # Проигрышная позиция для ИИ
        
        # Оцениваем позицию по количеству шашек и их расположению
        score = 0
        
        # Ценность шашек
        score += board.white_count * 10  # Обычные шашки ИИ
        score -= board.black_count * 10  # Обычные шашки противника
        
        # Подсчитываем дамки
        white_kings = 0
        black_kings = 0
        
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                
                if piece == board.WHITE_KING:
                    white_kings += 1
                    score += 15  # Дамки ценнее обычных шашек
                elif piece == board.BLACK_KING:
                    black_kings += 1
                    score -= 15
                
                # Бонус за продвижение к краю доски (для превращения в дамку)
                if piece == board.WHITE:
                    score += (7 - row)  # Белые стремятся к верхнему краю (row = 0)
                elif piece == board.BLACK:
                    score -= row  # Черные стремятся к нижнему краю (row = 7)
                
                # Бонус за контроль центра доски
                if piece != board.EMPTY:
                    center_distance = abs(3.5 - row) + abs(3.5 - col)
                    if piece == board.WHITE or piece == board.WHITE_KING:
                        score += (4 - center_distance) * 0.5
                    else:
                        score -= (4 - center_distance) * 0.5
        
        # Бонус за наличие дамок
        score += white_kings * 20
        score -= black_kings * 20
        
        # Бонус за возможность взятия
        white_captures = len([move for move in board.get_all_possible_moves(board.WHITE) if len(move) > 4])
        black_captures = len([move for move in board.get_all_possible_moves(board.BLACK) if len(move) > 4])
        
        score += white_captures * 5
        score -= black_captures * 5
        
        return score
