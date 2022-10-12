from hashlib import new
from math import exp
import random
import numpy as np
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer


class AIPlayer:
    def __init__(self, player_number: int, time: int):
        """
        :param player_number: Current player number
        :param time: Time per move (seconds)
        """
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.time = time
        # Do the rest of your implementation here

    def expectimax(self , state: Tuple[np.array, Dict[int, Integer]] , current_depth : int , max_depth : int , maxi : bool) ->  Tuple[float , Tuple[int, bool]] : 

        # valid_actions = get_valid_actions(player_number = self.player_number ,  state = state)
        valid_actions = [] 
        if maxi : 
            valid_actions = get_valid_actions(player_number = self.player_number ,  state = state)
        else :
            valid_actions = get_valid_actions(player_number =(self.player_number +2)%3 + (self.player_number +1 ) %3 ,  state = state)


        
        # print(valid_actions)
        scores = get_pts(self.player_number , state[0])  - get_pts((self.player_number +2)%3 + (self.player_number +1 ) %3 , state[0]) 
        #checking terminal condition 
        if len(valid_actions) == 0 :
            return ( scores, (0 , True ))

        #checking if max depth has reached 

        #!!!!!!!!!!!!!!!!!! optimize / modify this ...... 


        if current_depth >= max_depth :
            return (scores, (0 , True ))
            
        else:
            highest_score = -10000000000            #float
            expected_score = 0                      #float


            best_move = random.choice(valid_actions) 

            for action in valid_actions:
                player_num = 0 
                if maxi : 
                    player_num = self.player_number 
                else :
                    player_num = (self.player_number +2)%3 + (self.player_number +1 ) %3
                board = state[0].copy()
                popout_moves = state[1]
                num_popouts = {1: Integer(Integer.get_int(popout_moves[1])), 2: Integer(Integer.get_int(popout_moves[2]))}
                column = action[0]
                is_popout = action[1] 
                if not is_popout:
                    if 0 in board[:, column]:
                        for row in range(1, board.shape[0]):
                            update_row = -1
                            if board[row, column] > 0 and board[row - 1, column] == 0:
                                update_row = row - 1
                            elif row == board.shape[0] - 1 and board[row, column] == 0:
                                update_row = row
                            if update_row >= 0:
                                board[update_row, column] = player_num
                                break
                    else:
                        err = 'Invalid move by player {}. Column {}'.format(player_num, column, is_popout)
                        raise Exception(err)
                else:
                    if 1 in board[:, column] or 2 in board[:, column]:
                        for r in range(board.shape[0] - 1, 0, -1):
                            board[r, column] = board[r - 1, column]
                        board[0, column] = 0
                    else:
                        err = 'Invalid move by player {}. Column {}'.format(player_num, column)
                        raise Exception(err)
                    # print(num_popouts[player_num])
                    num_popouts[player_num].decrement()
                
                new_scores , new_move = self.expectimax((board , num_popouts) , current_depth + 1  , max_depth  , not maxi )
                if maxi : 
                    if new_scores > highest_score :
                        best_move = action
                        highest_score = new_scores 
                else :
                    expected_score += new_scores
            if maxi :
                return (highest_score , best_move)
            else :
                expected_score = expected_score / len(valid_actions)
                return expected_score , best_move
                    




    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move
        This will play against either itself or a human player
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        # print(state[0])
        return self.expectimax(state , 0 , 3 , True )[1]

        # Do the rest of your implementation here
        # raise NotImplementedError('Whoops I don\'t know what to do')

    def get_expectimax_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move based on
        the Expecti max algorithm.
        This will play against the random player, who chooses any valid move
        with equal probability
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here
        # print(state[0])
        # print(self.expectimax(state , 0 , 3 , True )[1])

        return self.expectimax(state , 0 , 4 , True )[1]




        raise NotImplementedError('Whoops I don\'t know what to do')
