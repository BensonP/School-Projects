import numpy as np
import random as rand
import reversi
import copy

class ReversiBot:
    def __init__(self, move_num):
        self.move_num = move_num
        
    def make_move(self, state):
        '''
        This is the only function that needs to be implemented for the lab!
        The bot should take a game state and return a move.

        The parameter "state" is of type ReversiGameState and has two useful
        member variables. The first is "board", which is an 8x8 numpy array
        of 0s, 1s, and 2s. If a spot has a 0 that means it is unoccupied. If
        there is a 1 that means the spot has one of player 1's stones. If
        there is a 2 on the spot that means that spot has one of player 2's
        stones. The other useful member variable is "turn", which is 1 if it's
        player 1's turn and 2 if it's player 2's turn.

        ReversiGameState objects have a nice method called get_valid_moves.
        When you invoke it on a ReversiGameState object a list of valid
        moves for that state is returned in the form of a list of tuples.

        Move should be a tuple (row, col) of the move you want the bot to make.
        '''
        valid_moves = state.get_valid_moves()

        if not valid_moves:
            return None

        _, best_move = self.minimax(state, 9, True, state.turn, float('-inf'), float('inf'))  # Get best move from minimax

        return best_move
    
    def minimax(self, node, depth, maximizingPlayer, startingPlayer, alpha, beta):
        if depth == 0 or len(node.get_valid_moves()) == 0:
            return self.evaluate_board(node, startingPlayer), None

        valid_moves = node.get_valid_moves()
        if not valid_moves:
            return self.evaluate_board(node, startingPlayer), None  # No moves, evaluate current state
        if depth > 3:
            valid_moves.sort(key=lambda move: self.evaluate_board(self.simulate_move(node, move), startingPlayer), reverse=maximizingPlayer)

        best_move = None

        if maximizingPlayer:
            max_eval = float('-inf')
            for move in valid_moves:
                new_state = self.simulate_move(node, move)
                eval, _ = self.minimax(new_state, depth - 1, False, startingPlayer, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        
        else:
            min_eval = float('inf')
            for move in valid_moves:
                new_state = self.simulate_move(node, move)
                eval, _ = self.minimax(new_state, depth - 1, True, startingPlayer, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate_board(self, state, startingPlayer):
        '''
        Heuristic function for evaluating board state.
        Returns a score based on the number of pieces each player has.
        '''
        board = state.board
        player = state.turn
        opponent = 1 if startingPlayer == 2 else 2

        player_score = np.sum(board == player)
        opponent_score = np.sum(board == opponent)

        player_mobility = len(self.get_valid_moves_for_player(state, player))
        opponent_mobility = len(self.get_valid_moves_for_player(state, opponent))

        # Corner control
        player_corners = self.get_corner_control(board, player)
        opponent_corners = self.get_corner_control(board, opponent)

        # Edge control (weighted)
        player_edge = self.get_edge_control(board, player)
        opponent_edge = self.get_edge_control(board, opponent)

        # Evaluate based on different aspects
        score = (player_score - opponent_score) + \
            1.5 * (player_mobility - opponent_mobility) + \
            3 * (player_corners - opponent_corners) + \
            0.5 * (player_edge - opponent_edge)

        return score
    
    def simulate_move(self, state, move):
        new_state = copy.deepcopy(state)
        new_state.board[move] = state.turn
        # print("added a move at: " + str(move) + str(player) + "\n")
        # print(state.turn)
        
        self.flip_pieces(new_state, move)

        new_state.turn = 1 if new_state.turn == 2 else 2
        return new_state
    
    def flip_pieces(self, state, move):
        if self.move_num <= 2:
            return

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # Vertical & Horizontal
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal
        
        board = state.board
        player = state.turn
        opponent = 1 if player == 2 else 2
        row, col = move

        for dr, dc in directions:
            r, c = row + dr, col + dc
            pieces_to_flip = []

            # Traverse in the direction until an empty space or out of bounds
            while 0 <= r < 8 and 0 <= c < 8 and board[r, c] == opponent:
                pieces_to_flip.append((r, c))
                r += dr
                c += dc

            # If we reached a player piece, flip the captured pieces
            if 0 <= r < 8 and 0 <= c < 8 and board[r, c] == player:
                for flip_r, flip_c in pieces_to_flip:
                    board[flip_r, flip_c] = player  # Flip the pieces

    def get_valid_moves_for_player(self, state, player):
        return [move for move in state.get_valid_moves() if state.board[move] == 0]

    def get_corner_control(self, board, player):
        # Check the four corners for control (player's piece on the corner)
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        return sum(1 for corner in corners if board[corner] == player)

    def get_edge_control(self, board, player):
        # Check the edges (excluding corners) for control
        edge_positions = [
            (0, i) for i in range(1, 7)] + [(7, i) for i in range(1, 7)] + \
            [(i, 0) for i in range(1, 7)] + [(i, 7) for i in range(1, 7)]
        return sum(1 for pos in edge_positions if board[pos] == player)


