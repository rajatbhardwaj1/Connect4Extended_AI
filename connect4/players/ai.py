import math
import random
from time import time
import numpy as np
import copy
from typing import List, Tuple, Dict, Union

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
        self.alpha = 200
        self.best_action = None
        self.start = None
        # Do the rest of your implementation here

    def get_diagonals_primary(self, board: np.array) -> List[int]:
        m, n = board.shape
        for k in range(n + m - 1):
            diag = []
            for j in range(max(0, k - m + 1), min(n, k + 1)):
                i = k - j
                diag.append(board[i, j])
            yield diag


    def get_diagonals_secondary(self, board: np.array) -> List[int]:
        m, n = board.shape
        for k in range(n + m - 1):
            diag = []
            for x in range(max(0, k - m + 1), min(n, k + 1)):
                j = n - 1 - x
                i = k - x
                diag.append(board[i][j])
            yield diag
    


    def get_row_score(self , player_number: int, row: Union[np.array, List[int]]):
        score = {0:0 , 1 :0 , 2 :0 , 3:0 , 4:0}
        n = len(row)
        j = 0
        while j < n:
            if row[j] == player_number:
                count = 0
                while j < n and row[j] == player_number:
                    count += 1
                    j += 1
                k = 4
                if count >= 4 : 
                    score[4] = (count // k) 
                score[count%k] += 1 
            else:
                j += 1
        return score


        
        
    def eval(self , player_number: int, board: np.array):
        
        score = 0
        m, n = board.shape

        #centre pref 

        
        temp = self.get_row_score(player_number, board[:, 4])
        score += 10*temp[4] + 7*temp[3] + 4*temp[2] + 2*temp[1]
        

        # score in rows
        for i in range(m):
            temp = self.get_row_score(player_number, board[i])
            score += 150*temp[4] + 10*temp[3] + 2*temp[2]
        # score in columns
        for j in range(n):
            temp = self.get_row_score(player_number, board[:, j])
            score += 150*temp[4] + 10*temp[3] + 2*temp[2] 
        # scores in diagonals_primary
        for diag in self.get_diagonals_primary(board):
            temp = self.get_row_score(player_number, diag)
            score += 150*temp[4] + 10*temp[3] + 2*temp[2] 
        # scores in diagonals_secondary
        for diag in self.get_diagonals_secondary(board):
            temp =  self.get_row_score(player_number, diag)
            score += 150*temp[4] + 10*temp[3] + 2*temp[2] 
        
        
        player_number_1 = (self.player_number +2)%3 + (self.player_number +1 ) %3
        # score in rows
        for i in range(m):
            temp = self.get_row_score(player_number_1, board[i])
            score += -600*temp[4]  -100*temp[3] 
        # score in columns
        for j in range(n):
            temp = self.get_row_score(player_number_1, board[:, j])
            score += -600*temp[4]  -100*temp[3] 
        # scores in diagonals_primary
        for diag in self.get_diagonals_primary(board):
            temp = self.get_row_score(player_number_1, diag)
            score +=-600*temp[4]  -100*temp[3] 
        # scores in diagonals_secondary
        for diag in self.get_diagonals_secondary(board):
            temp =  self.get_row_score(player_number_1, diag)
            score += -600*temp[4]  -100*temp[3] 
        return score

 
        
    def update_board(self, state : Tuple[np.array, Dict[int, Integer]], player_num: int, action : Tuple[int, bool]):
      column, is_popout = action
      board, num_popouts = state
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
      else:
        if 1 in board[:, column] or 2 in board[:, column]:
          for r in range(board.shape[0] - 1, 0, -1):
            board[r, column] = board[r - 1, column]
          board[0, column] = 0
        num_popouts[player_num].decrement()

###############################################################################################
    """
    Implement iterative deepening
    Increase alpha or beta?
    """
    def minimax(self, player_number, state, depth):
      if (time()-self.start > self.time-0.5):
        return None,None
      actions = get_valid_actions(player_number, state)
      random.shuffle(actions)
      if (not actions):
        return 0, None
      if (not depth):
        return 0, actions[0]
      curr_diff = get_pts(player_number, state[0]) - get_pts(3-player_number, state[0])
      max_diff = -math.inf
      max_action = None
      for action in actions:
        next_state = np.copy(state[0]), copy.deepcopy(state[1])
        self.update_board(next_state, player_number,action)
        val = self.minimax(3-player_number, next_state, depth-1)
        if (val == (None,None)):
          return val
        next_diff = get_pts(player_number, next_state[0]) - get_pts(3-player_number, next_state[0]) 
        diff = -val[0] + next_diff - curr_diff
        if (diff >= self.alpha):
          return diff, action
        if (diff> max_diff):
          max_diff = diff
          max_action = action
      return max_diff, max_action 

    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
      self.start = time()
      max_depth = 0
      while (True):
        temp = self.minimax(self.player_number, state, max_depth)
        if (temp == (None,None) or max_depth > 20):
          if (self.best_action[1]):
            print(str(self.best_action[0])+"P")
          else:
            print(self.best_action[0])
          return self.best_action
        self.best_action = temp[1]
        max_depth+=1
    def expectimax(self , state: Tuple[np.array, Dict[int, Integer]] , current_depth : int , max_depth : int , maxi : bool , end_time  ) ->  Tuple[float , Tuple[int, bool]] : 
        max_beam = 8

        scores = self.eval(self.player_number , state[0])

        valid_actions = [] 

        if maxi : 
            valid_actions = get_valid_actions(player_number = self.player_number ,  state = state)
        else :
            valid_actions = get_valid_actions(player_number =(self.player_number +2)%3 + (self.player_number +1 ) %3 ,  state = state)

        if len(valid_actions) == 0 :
            return ( scores, (0 , True ))

        if current_depth >= max_depth :
            return (scores, (0 , True ))
            
        else:
            highest_score = -10000000000            #float
            expected_score = 0                      #float

            best_move = random.choice(valid_actions) 

      
            if time() + 0.5 > end_time:
                return scores , (0 , True )      
            beam_size = 0 
            for action in valid_actions:
                player_num = 0 
                if maxi : 
                    player_num = self.player_number 
                else :
                    player_num = 3 - self.player_number 
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
                    num_popouts[player_num].decrement()
         
                new_scores , new_move = self.expectimax((board , num_popouts) , current_depth + 1  , max_depth  , not maxi  , end_time )
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
 
        valid_actions = get_valid_actions(player_number = self.player_number ,  state = state)

        best_move = random.choice(valid_actions) 

        end_time = time()  + self.time
        i = 3
        while(time() < end_time - 0.5):

            new_score ,new_best = self.expectimax(state , 0 , i , True , end_time )
            i += 1
            print(i)
            if time() < end_time - 0.5:
                best_move = new_best
            if i > 100:
                break
            
        print(get_pts(self.player_number , state[0]) , get_pts((self.player_number +2)%3 + (self.player_number +1 ) %3 , state[0]))

        return best_move
