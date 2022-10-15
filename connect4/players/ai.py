from hashlib import new
from math import exp
from operator import le
import random
from time import time
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
    

    
    def expectimax(self , state: Tuple[np.array, Dict[int, Integer]] , current_depth : int , max_depth : int , maxi : bool , curr_score : float , end_time , left_right ) ->  Tuple[float , Tuple[int, bool]] : 
        max_beam = 10 -  current_depth

        scores = get_pts(self.player_number , state[0])  


        scores -= get_pts((self.player_number +2)%3 + (self.player_number +1 ) %3 , state[0]) 

        scores -= curr_score 
        if current_depth > 0 :
            scores /= current_depth
        



        # if current_depth == 1 :
        #     print(scores )

        
      

        # valid_actions = get_valid_actions(player_number = self.player_number ,  state = state)
        valid_actions = [] 
        if maxi : 
            valid_actions = get_valid_actions(player_number = self.player_number ,  state = state)
      


            if len(valid_actions) > max_beam and (current_depth == 0 or current_depth == 1) : 
                
                pop_moves = [] 
                not_pop_move  = [] 
                for action in valid_actions: 
                    if action[1] == True: 
                        pop_moves.append(action)
                    else :
                        not_pop_move.append(action)
                if left_right >=  6  and left_right <9:
                    not_pop_move.reverse() 
                
                    
                temp = [] 
                if left_right != 9 and left_right != 0 :
                    for i in range (0 , max_beam - 4 // max(1 , current_depth)):
                        if i < len(not_pop_move):

                            temp.append(not_pop_move[i])
                        else :
                            temp.append(valid_actions[i])
                    
                # random.shuffle(valid_actions)
                # temp.append(valid_actions[0])

               
                
                    # elif action[1] == False and i >= max_beam - 3 // max(1 , current_depth) :
                    #     not_pop_move.append(action)
                # random.shuffle(not_pop_move)
                random.shuffle(pop_moves)
                # pop_moves.reverse()

               
                
                # if len(not_pop_move) > 0:
                #     temp.append(not_pop_move[0])

                for action in pop_moves:
                    temp.append(action)
                    if len(temp) > max_beam:
                        break
                i = 0 
                while len(temp) < max_beam:
                    temp.append(not_pop_move[i])
                    i += 1 
                valid_actions = temp
            #     # print(valid_actions)
            # random.shuffle(valid_actions)
            
        else :
            
            valid_actions = get_valid_actions(player_number =(self.player_number +2)%3 + (self.player_number +1 ) %3 ,  state = state)
            random.shuffle(valid_actions) 
        
        # random.shuffle(valid_actions)
        
        # print(valid_actions)
        
        
        

        # if curr_score == 0 : 
        #     scores  = scores - curr_score 
        # else :
        #     scores = (scores - curr_score )/ curr_score
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

            if not maxi :
                if scores < 0 :
                    return scores , (0 , True )

            if time() + 0.5 > end_time:
                return 10000000 , best_move 
             
            beam_size = 0 

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
                
                new_scores , new_move = self.expectimax((board , num_popouts) , current_depth + 1  , max_depth  , not maxi , curr_score , end_time ,left_right)
                if maxi : 
                    if new_scores > highest_score :
                        best_move = action
                        highest_score = new_scores 
                        
                else :

                    expected_score += new_scores
                    
                beam_size += 1 

                if beam_size == max_beam :
                    break
            
            if maxi :
                return (highest_score , best_move)
            else :
                expected_score = expected_score / len(valid_actions)
                return expected_score , best_move
                    

    def minimax(self , state: Tuple[np.array, Dict[int, Integer]] , current_depth : int , max_depth : int , maxi : bool , curr_score : float , end_time , alpha : int , beta : int , last_action: int  ) ->  Tuple[float , Tuple[int, bool]] : 
        
        max_beam = 10 -  current_depth

        scores = get_pts(self.player_number , state[0])  


        scores -= get_pts((self.player_number +2)%3 + (self.player_number +1 ) %3 , state[0]) 

        scores -= curr_score 
        if current_depth > 0 :
            scores /= current_depth 
        

        valid_actions = [] 

        if maxi : 
            valid_actions = get_valid_actions(player_number = self.player_number ,  state = state)
      
        else :

            valid_actions = get_valid_actions(player_number =(self.player_number +2)%3 + (self.player_number +1 ) %3 ,  state = state)
             

        if len(valid_actions) == 0 :
            return ( scores, (0 , True ))
        
        

        # temp = [] 

        # window_ind = max(0 , last_action - max_beam // 2 )
        # while window_ind < max_beam and window_ind < len(valid_actions) :
        #     temp.append(valid_actions[window_ind])
        #     window_ind += 1 
        # valid_actions = temp



        #checking if max depth has reached 

        #!!!!!!!!!!!!!!!!!! optimize / modify this ...... 


        if current_depth >= max_depth :
            return (scores, (0 , True ))
            
        else:
            highest_score = -10000000000            #float
            least_score = 0                      #float

            best_move = random.choice(valid_actions) 
            beam_size = 0 

            for action in valid_actions:

                player_num = 0 
                value =0 
                if maxi : 
                    player_num = self.player_number 
                    value = -10000000
                else :
                    player_num = (self.player_number +2)%3 + (self.player_number +1 ) %3
                    value = 10000000

                
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
                
                new_scores , new_move = self.minimax((board , num_popouts) , current_depth + 1  , max_depth  , not maxi , curr_score  , end_time , alpha , beta , action[0])
                if maxi : 
                    value = max( value , new_scores )
                    if value >= beta :
                        break
                    alpha = max( alpha , value )
                    if new_scores > highest_score :
                        best_move = action
                        highest_score = new_scores 
                else :
                    value = min(value , new_scores )
                    if value <= alpha:
                        # print('pruning !!!!')
                        break
                    beta = min(beta , value )
                    if least_score < new_scores : 
                        best_move = action 
                        least_score = new_scores 

                    
            
            if maxi :
                return (highest_score , best_move)
            else :
                return (least_score , best_move)
                    

        pass


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
        current_scores = get_pts(self.player_number , state[0]) - get_pts((self.player_number +2)%3 + (self.player_number +1 ) %3 , state[0])

        valid_actions = get_valid_actions(player_number = self.player_number ,  state = state)

        best_move = random.choice(valid_actions) 
        score = 0 

        end_time = time()  + self.time
        i = 3
        # while(time() < end_time - 0.5):

        #     new_score ,new_best    = self.expectimax(state , 0 , i , True , current_scores_enemy, end_time)
        #     if score > new_score :
        #         score = new_score
        #         best_move = new_best 
            


        alpha = -10000000 
        beta = 10000000
        scores , move = self.minimax(state , 0 , 5, True , current_scores, end_time , alpha , beta , -1 ) 

        return move
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
        # print('l')
        current_scores = get_pts(self.player_number , state[0]) - get_pts((self.player_number +2)%3 + (self.player_number +1 ) %3 , state[0])

        valid_actions = get_valid_actions(player_number = self.player_number ,  state = state)

        best_move = random.choice(valid_actions) 
        score = 0 

        end_time = time()  + self.time
        i = 3

        left_right = random.randint(0, 9)



        # while(time() < end_time - 0.5):

        #     new_score ,new_best = self.expectimax(state , 0 , i , True , current_scores, end_time , left_right)
        #     i += 1
            
        #     if new_score != 10000000:
        #         best_move = new_best 
            
        if left_right == 9 or left_right == 0 :
            print('popmove!!!')
        return self.expectimax(state , 0 , i + 2 , True , current_scores, end_time , left_right)[1]




        raise NotImplementedError('Whoops I don\'t know what to do')
