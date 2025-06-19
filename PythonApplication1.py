# -*- coding: utf-8 -*-
class CheckersGame:
    def __init__(self):
        self.board = []
        self.current_player = 'W'
        self.initialize_board()
    
    def initialize_board(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        
        # White pieces (top)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = 'W'
        
        # Black pieces (bottom)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = 'B'
    
    def print_board(self):
        print("  a b c d e f g h")
        print(" +-----------------+")
        
        for i, row in enumerate(self.board):
            print(f"{8-i}|", end="")
            for cell in row:
                symbol = cell[0] if cell != ' ' else ' '
                print(f"{symbol}|", end="")
            print(f"{8-i}")
            print(" +-----------------+")
        
        print("  a b c d e f g h")
    
    def is_valid_position(self, pos):
        if len(pos) != 2:
            return False
        col, row = pos[0], pos[1]
        return col in 'abcdefgh' and row in '12345678'
    
    def convert_position(self, pos):
        col_map = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        x = 8 - int(pos[1])
        y = col_map[pos[0]]
        return x, y
    
    def get_moves(self, x, y):
        moves = []
        piece = self.board[x][y]
        
        directions = []
        if piece == 'W':
            directions = [(-1, -1), (-1, 1)]
        elif piece == 'B':
            directions = [(1, -1), (1, 1)]
        elif piece in ['WK', 'BK']:  # Kings
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        # Normal moves
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if self.board[nx][ny] == ' ':
                    moves.append((nx, ny, None))
        
        # Capture moves
        for dx, dy in directions:
            nx, ny = x + 2*dx, y + 2*dy
            jx, jy = x + dx, y + dy
            
            if 0 <= nx < 8 and 0 <= ny < 8:
                if self.board[nx][ny] == ' ':
                    jump_piece = self.board[jx][jy]
                    if (piece == 'W' and jump_piece.startswith('B')) or \
                       (piece == 'B' and jump_piece.startswith('W')) or \
                       (piece == 'WK' and jump_piece.startswith('B')) or \
                       (piece == 'BK' and jump_piece.startswith('W')):
                        moves.append((nx, ny, (jx, jy)))
        
        return moves
    
    def has_captures(self, player):
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if player == 'W' and piece in ['W', 'WK']:
                    if any(move[2] for move in self.get_moves(x, y)):
                        return True
                elif player == 'B' and piece in ['B', 'BK']:
                    if any(move[2] for move in self.get_moves(x, y)):
                        return True
        return False
    
    def make_move(self, start, end, capture):
        sx, sy = start
        ex, ey = end
        piece = self.board[sx][sy]
        
        self.board[ex][ey] = piece
        self.board[sx][sy] = ' '
        
        if capture:
            cx, cy = capture
            self.board[cx][cy] = ' '
        
        # Promote to king
        if piece == 'W' and ex == 0:
            self.board[ex][ey] = 'WK'
        elif piece == 'B' and ex == 7:
            self.board[ex][ey] = 'BK'
    
    def play(self):
        print("Welcome to Checkers!")
        print("Players: W (White) and B (Black)")
        print("Enter moves like 'e2 e3'")
        
        while True:
            self.print_board()
            print(f"Current player: {'White (W)' if self.current_player == 'W' else 'Black (B)'}")
            
            must_capture = self.has_captures(self.current_player)
            valid_move = False
            
            while not valid_move:
                move_input = input("Your move: ").split()
                if len(move_input) != 2:
                    print("Invalid format. Use: 'e2 e3'")
                    continue
                
                start, end = move_input
                
                if not (self.is_valid_position(start) and self.is_valid_position(end)):
                    print("Invalid positions. Use format like 'e5'")
                    continue
                
                sx, sy = self.convert_position(start)
                ex, ey = self.convert_position(end)
                
                piece = self.board[sx][sy]
                if (self.current_player == 'W' and piece not in ['W', 'WK']) or \
                   (self.current_player == 'B' and piece not in ['B', 'BK']):
                    print("Select your piece!")
                    continue
                
                moves = self.get_moves(sx, sy)
                found = False
                capture_pos = None
                
                for move in moves:
                    if move[0] == ex and move[1] == ey:
                        found = True
                        capture_pos = move[2]
                        break
                
                if not found:
                    print("Invalid move!")
                    continue
                
                if must_capture and not capture_pos:
                    print("You must capture!")
                    continue
                
                self.make_move((sx, sy), (ex, ey), capture_pos)
                valid_move = True
                
                if capture_pos:
                    print(f"Captured piece at {chr(capture_pos[1]+97)}{8-capture_pos[0]}!")
            
            # Check win
            white_exists = any('W' in row or 'WK' in row for row in self.board)
            black_exists = any('B' in row or 'BK' in row for row in self.board)
            
            if not white_exists:
                self.print_board()
                print("Black wins!")
                break
            if not black_exists:
                self.print_board()
                print("White wins!")
                break
            
            self.current_player = 'B' if self.current_player == 'W' else 'W'

if __name__ == "__main__":
    game = CheckersGame()
    game.play()