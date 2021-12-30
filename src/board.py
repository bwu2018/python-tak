from piece import Piece
from stack import Stack
from utils import ij_to_ptn, findCombinations, ptn_to_ij

# board_dim: (num_stones, num_capstones)
pieces = {3: (10, 0), 4: (15, 0), 5: (21, 1), 6: (30, 1), 8: (50, 2)}

class Board():
    def __init__(self, dim):
        self.dim = dim
        self.white_stones_remaining = pieces[dim][0]
        self.black_stones_remaining = pieces[dim][0]
        self.white_capstones_remaining = pieces[dim][1]
        self.black_capstones_remaining = pieces[dim][1]
        self.board = [[Stack()] * dim for _ in range(dim)]
        self.current_player = 1 # White=1, Black=0
        self.moves = []
        self.directions = ['-', '+', '<', '>']
    
    def __str__(self):
        return ' '.join(self.moves)

    def legal_moves(self):
        all_moves = []
        
        for i, row in self.board:
            for j, col in row:
                # Get placement moves
                if col.top is None:
                    if self.current_player == 1:
                        if self.white_stones_remaining > 0:
                            all_moves.append(ij_to_ptn(i, j, self.dim))
                            all_moves.append('S' + ij_to_ptn(i, j, self.dim))
                        if self.white_capstones_remaining > 0:
                            all_moves.append('C' + ij_to_ptn(i, j, self.dim))
                    if self.current_player == 0:
                        if self.black_stones_remaining > 0:
                            all_moves.append(ij_to_ptn(i, j, self.dim))
                            all_moves.append('S' + ij_to_ptn(i, j, self.dim))
                        if self.black_capstones_remaining > 0:
                            all_moves.append('C' + ij_to_ptn(i, j, self.dim))

                # Get all possible moves from current stacks
                # TODO: Still need to handle case in which capstone flattens standing stone
                if col.top_color == self.current_player:
                    stack_size = min(col.top.length(), 5)
                    possible_squares = [0, 0, 0, 0]
                    for square in range(stack_size):
                        # Down
                        if i + square < self.dim and self.board[i + square][j].top.piece_type == 'F':
                            possible_squares[0] += 1
                        # Up
                        if i - square > 0 and self.board[i - square][j].top.piece_type == 'F':
                            possible_squares[1] += 1
                        # Left
                        if j - square > 0 and self.board[i][j - square].top.piece_type == 'F':
                            possible_squares[2] += 1
                        # Right
                        if j + square < self.dim and self.board[i][j + square].top.piece_type == 'F':
                            possible_squares[3] += 1
                    for x in range(4):
                        if possible_squares[x] == 0:
                            continue
                        elif possible_squares[x] == 1:
                            all_moves.append(ij_to_ptn(i, j, self.dim) + self.directions[x])
                        else:
                            for string in findCombinations(possible_squares[x]):
                                all_moves.append(possible_squares[x] + ij_to_ptn(i, j, self.dim) + self.directions[x] + string)
        return all_moves

    def push_move(self, move):
        if move not in self.legal_moves(self):
            return False
        self.moves.push(move)
        for direction in self.directions:
            if direction in move:
                if move[0].isdigit():
                    i, j = ptn_to_ij(move[1:2])
                    temp_stack = []
                    for _ in range(move[0]):
                        temp_stack.append(self.board[i][j].pop())
                    for stones in move[4:]:
                        stones_to_drop = int(stones)
                        if direction == '-':
                            i += stones_to_drop
                        elif direction == '+':
                            i -= stones_to_drop
                        elif direction == '<':
                            j -= stones_to_drop
                        elif direction == '>':
                            j += stones_to_drop
                        for _ in range(stones_to_drop):
                            self.board[i][j].stack.push(temp_stack.pop(len(temp_stack)))
                else:
                    i, j = ptn_to_ij(move[0:1])
                    temp_stack = []
                    temp_stack.append(self.board[i][j].pop())
                    stones_to_drop = 1
                    if direction == '-':
                        i += stones_to_drop
                    elif direction == '+':
                        i -= stones_to_drop
                    elif direction == '<':
                        j -= stones_to_drop
                    elif direction == '>':
                        j += stones_to_drop
                    self.board[i][j].stack.push(temp_stack.pop(len(temp_stack)))
        if len(move) == 2:
            i, j = ptn_to_ij(move)
            self.board[i][j].stack.push(Piece('F', self.current_player))
        elif move[0] == 'S':
            i, j = ptn_to_ij(move[1:2])
            self.board[i][j].stack.push(Piece('S', self.current_player))
        elif move[0] == 'C':
            i, j = ptn_to_ij(move[1:2])
            self.board[i][j].stack.push(Piece('C', self.current_player))
        self.current_player = not self.current_player
        return True

    # def pop(self):
    #     self.moves.pop()

    def is_game_end(self):
        if self.is_road_win() and self.is_flats_win():
            return True
        else:
            return False

    def is_road_win(self):
        # TODO:
        return None

    def is_flats_win(self):
        # TODO:
        if (self.white_stones_remaining == 0 and self.white_capstones_remaining == 0) or (self.black_stones_remaining == 0 and self.black_capstones_remaining ==0):
            return True
        

    # ptn: portable tak notation
    def load(self, ptn):
        for move in ptn:
            self.push_move(self, move)