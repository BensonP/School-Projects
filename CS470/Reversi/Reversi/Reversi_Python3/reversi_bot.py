import numpy as np
import random as rand
import reversi

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


        print(valid_moves)

        move = rand.choice(valid_moves) # Moves randomly...for now
        return move
    
    def minimax(self, node, depth, maximizingPlayer):
        '''
        Minimax algorithm with depth limit.
        '''
        if depth == 0 or node.is_game_over():
            return self.evaluate_board(node)

        valid_moves = node.get_valid_moves()
        if not valid_moves:
            return self.evaluate_board(node)  # No moves, evaluate current state

        if maximizingPlayer:
            max_eval = float('-inf')
            for move in valid_moves:
                new_state = node.simulate_move(move)
                eval = self.minimax(new_state, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                new_state = node.simulate_move(move)
                eval = self.minimax(new_state, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def evaluate_board(self, state):
        '''
        Heuristic function for evaluating board state.
        Returns a score based on the number of pieces each player has.
        '''
        board = state.board
        p1_score = np.sum(board == 1)
        p2_score = np.sum(board == 2)
        return p1_score - p2_score  # Higher is better for Player 1, lower is better for Player 2
    
    def simulate_move(state, move, player)
        state.board(move) = player


    def max(valid_moves):
        for x in valid_moves:
